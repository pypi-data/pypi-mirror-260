from ftplib import FTP, error_perm
from typing import Optional, Union, Literal

import io, os, socket, re

try: import Filter
except ImportError: from . import Filter

class FTPError(Exception):
    """Custom exception for FTP errors."""
    pass

class EasyFTP:
    def __init__(self) -> None:
        self.ftp: Optional[FTP] = None

    def __enter__(self) -> 'EasyFTP':
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.ftp:
            self.ftp.quit()

    def connect(self, host: str, port: int, username: str, password: str, timeout: int = None) -> int:
        if type(port) != int: raise FTPError("port must be integer type.") from None
        """Connect to the FTP server."""
        try:
            self.ftp = FTP()
            self.ftp.connect(host, port, timeout=timeout)
            self.ftp.login(username, password)
            return 1
        except socket.timeout:
            raise FTPError(f"Connection to {host}:{port} timed out") from None
        except Exception as e:
            raise FTPError(f"Error occured during connection to server: {e}") from None

    def write(self, remote_path: str, content: str) -> None:
        """Write content to a remote file."""
        try:
            self.ftp.storlines('STOR ' + remote_path, io.BytesIO(content.encode()))
        except error_perm as e:
            raise FTPError(f"Error while writing file: {e}") from None

    def read(self, remote_path: str) -> str:
        """Read content from a remote file."""
        try:
            output = io.StringIO()
            self.ftp.retrlines("RETR " + remote_path, output.write)
            result = output.getvalue()
            return result
        except error_perm as e:
            raise FTPError(f"Error while reading file: {e}") from None
        
    def delete(self, filename: str, filt : Optional[Filter.Filter] = None, path : Optional[str] = None) -> None:
        """Delete a file or files from the FTP server."""
        if filt is not None:
            if path is None: raise FTPError("parameter path must be provided when using filter in EasyFTP.delete method.") from None
            pwd = self.pwd(); self.cd(path)
            for file in self.ls(path):
                try:
                    if (incl := filt.matches_patterns(filt.incl, file)):
                        self.ftp.delete(file)
                        print(f"Deleted file '{file}' from remote since it matches with include filter {incl}."); continue
                    # else:
                    #    print(f"Did not delete file '{file}' from remote since it does not match with include filter {incl}."); continue
                except error_perm as e:
                    print(f"Error occured while deleting file {file}: {str(e).split('\n')[0]}")
            self.cd(pwd)
        else:
            try:
                self.ftp.delete(filename)
                print(f"Deleted file: {filename}")
            except error_perm as e:
                raise FTPError(f"Error while deleting file: {e}") from None

    def mkdir(self, path: str) -> None:
        """Create a directory on the FTP server."""
        try:
            self.ftp.mkd(path)
        except error_perm as e:
            raise FTPError(f"Error while creating directory: {e}") from None

    def cd(self, path: Optional[str] = None) -> str:
        """Change current directory on the FTP server."""
        try:
            if path is not None:
                self.ftp.cwd(path)
                return path
            else:
                return self.ftp.pwd()
        except error_perm as e:
            raise FTPError(f"Error while changing directory: {e}") from None

    def pwd(self) -> str:
        """Get the current directory on the FTP server."""
        try:
            return self.ftp.pwd()
        except error_perm as e:
            raise FTPError(f"Error while getting current directory: {e}") from None

    def ls(self, path: Optional[str] = None) -> list:
        """List files in the current or specified directory."""
        try:
            if path is not None:
                self.ftp.cwd(path)
            files = self.ftp.nlst()
            return files
        except error_perm as e:
            raise FTPError(f"Error while listing directory: {e}") from None

    def download(self, remote_path: str, local_path: str, filt : Optional[Filter.Filter] = None) -> None:
        """Download a file or directory from the FTP server."""
        remote_path = remote_path.replace("\\", "/")
        local_path = local_path.replace("\\", "/")
        try:
            if self.is_dir(remote_path):
                # Create the local directory if it doesn't exist
                os.makedirs(local_path, exist_ok=True)

                # Get list of files and directories in remote directory
                self.cd(remote_path)
                files = self.ls()

                for file in files:
                    remote_file_path = os.path.join(remote_path, file).replace("\\", "/")
                    local_file_path = os.path.join(local_path, file).replace("\\", "/")

                    if self.is_dir(remote_file_path):
                        self.download(remote_file_path, local_file_path)
                    else:
                        if filt:
                            if (ex := filt.matches_patterns(filt.excl, remote_file_path)):
                                print(f"Not downloaded file '{local_file_path}' to local since it matches with exclude filter {ex}."); continue
                            
                        
                        try:
                            with open(local_file_path, 'wb') as local_file:
                                self.ftp.retrbinary('RETR ' + remote_file_path, local_file.write)
                        except error_perm as e:
                            print(f"Error occured during downloading {remote_file_path}: {str(e).split('\n')[0]}")
                        else:
                            print(f"Downloaded file '{remote_file_path}' to '{local_file_path}'")

                print(f"Recursive download from '{remote_path}' to '{local_path}' completed.")
            else:
                with open(local_path, 'wb') as local_file:
                    self.ftp.retrbinary('RETR ' + remote_path, local_file.write)

                print(f"Downloaded file '{remote_path}' to '{local_path}'")
        except error_perm as e:
            raise FTPError(f"Error while downloading file or directory: {e}") from None

    def is_dir(self, path: str) -> bool:
        """Check if the given path is a directory."""
        try:
            # Use NLST command to list directory contents
            contents = self.ftp.nlst(path)
            
            # If NLST didn't raise an error, then the path is likely a directory
            return True
        except error_perm as e:
            # If NLST raised an error, it means the path is not a directory
            return False
        except Exception as e:
            raise FTPError(f"Error while checking if path '{path}' is a directory: {e}")

    def upload(self, local_path: str, remote_path: str, filt : Optional[Filter.Filter] = None) -> None:
        """Upload a file or directory to the FTP server."""
        try:
            if os.path.isdir(local_path):

                # Iterate through local directory and upload files
                for root, dirs, files in os.walk(local_path):
                    for file in files:
                        local_file_path = os.path.join(root, file).replace("\\", "/")
                        remote_file_path = os.path.join(remote_path, os.path.relpath(local_file_path, local_path))

                        if filt:
                            if (ex := filt.matches_patterns(filt.excl, local_file_path)):
                                print(f"Not uploaded file '{local_file_path}' to remote since it matches with exclude filter {ex}.")
                                continue

                        try:
                            with open(local_file_path, 'rb') as local_file:
                                self.ftp.storbinary('STOR ' + remote_file_path, local_file)
                        except error_perm as e:
                            print(f"Error occured during uploading {remote_file_path}: {str(e).split('\n')[0]}")
                        else:
                            print(f"Uploaded file '{local_file_path}' to '{remote_file_path}'")

                print(f"Recursive upload from '{local_path}' to '{remote_path}' completed.")
            else:
                with open(local_path, 'rb') as local_file:
                    self.ftp.storbinary('STOR ' + remote_path, local_file)

                print(f"Uploaded file '{local_path}' to '{remote_path}'")
        except FileNotFoundError:
            raise FTPError(f"Local file or directory '{local_path}' not found") from None
        except error_perm as e:
            raise FTPError(f"Error while uploading file or directory: {e}") from None

    def rename(self, from_name: str, to_name: str) -> None:
        """Rename a file on the FTP server."""
        try:
            self.ftp.rename(from_name, to_name)
            print(f"Renamed file '{from_name}' to '{to_name}'")
        except error_perm as e:
            raise FTPError(f"Error while renaming file: {e}") from None
        
    def mv(self, origin: str, dest: str) -> None:
        """Move/rename a file or directory on the FTP server."""
        try:
            self.ftp.rename(origin, dest)
            print(f"Moved/Renamed '{origin}' to '{dest}'")
        except error_perm as e:
            raise FTPError(f"Error while moving/renaming file or directory: {e}") from None
    
    def chmod(self, remote_path: str, perm: int, mode: Literal["oct", "bin", "int"] = "int") -> None:
        """
        Edit permissions of a file on the FTP server.
        The FTP server MUST support SITE command.
        """
        if mode == "int":
            if not (0 <= perm <= 777):
                raise FTPError("perm should be 0 <= perm <= 777 when in 'int' mode.")
        elif mode == "oct":
            if not (0o0 <= perm <= 0o777):
                raise FTPError("perm should be 0o0 <= perm <= 0o777 when in 'oct' mode.")
            else: perm = int(oct(perm)[2:])
        elif mode == "bin":
            if not (0b000000000 <= perm <= 0b111111111):
                raise FTPError("perm should be 0b000000000 <= perm <= 0b111111111 when in 'bin' mode.")
            else: perm = 100 * int((b := bin(perm)[2:])[0:3], 2) + 10 * int(b[3:6], 2) + int(b[6:9], 2)
        else:
            raise FTPError(f"permission mode unsupported : {mode}. mode can be 'int', 'oct', or 'bin'.")
        
        try:
            self.ftp.sendcmd("SITE CHMOD %d %s" % (perm, remote_path))
        except error_perm as e:
            raise FTPError(f"Error while changing permission of file: {e}") from None; return 0
        else: return 1

if __name__ == "__main__":
    import os
    with EasyFTP() as session:
        session.connect("localhost", 21, "admin", os.environ['ftppassword'])

        f = Filter.Filter(include = r"de.d")
        session.delete(".", f, ".")