from ftplib import FTP, error_perm
import io, os, socket
from typing import Optional

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
        """Connect to the FTP server."""
        try:
            self.ftp = FTP()
            self.ftp.connect(host, port, timeout=timeout)
            self.ftp.login(username, password)
            return 1
        except socket.timeout:
            raise FTPError(f"Connection to {host}:{port} timed out") from None
        except Exception:
            return 0

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
        
    def delete(self, filename: str) -> None:
        """Delete a file from the FTP server."""
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

    def download(self, remote_path: str, local_path: str) -> None:
        """Download a file or directory from the FTP server."""
        remote_path = remote_path.replace("\\", "/")
        try:
            if self.is_dir(remote_path):
                # Create the local directory if it doesn't exist
                os.makedirs(local_path, exist_ok=True)

                # Get list of files and directories in remote directory
                print(remote_path)
                self.cd(remote_path)
                files = self.ls()

                for file in files:
                    remote_file_path = os.path.join(remote_path, file)
                    local_file_path = os.path.join(local_path, file)

                    if self.is_dir(remote_file_path):
                        self.download(remote_file_path, local_file_path)
                    else:
                        with open(local_file_path, 'wb') as local_file:
                            self.ftp.retrbinary('RETR ' + remote_file_path, local_file.write)

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

    def upload(self, local_path: str, remote_path: str) -> None:
        """Upload a file or directory to the FTP server."""
        try:
            if os.path.isdir(local_path):

                # Iterate through local directory and upload files
                for root, dirs, files in os.walk(local_path):
                    for file in files:
                        local_file_path = os.path.join(root, file).replace("\\", "/")
                        remote_file_path = os.path.join(remote_path, os.path.relpath(local_file_path, local_path))

                        with open(local_file_path, 'rb') as local_file:
                            self.ftp.storbinary('STOR ' + remote_file_path, local_file)

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