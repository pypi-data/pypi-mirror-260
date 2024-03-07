import re

from typing import *

class FilterError(Exception):
    pass

class Filter:
    def __init__(self, include: Union["str", "list"] = None, exclude: Union["str", "list"] = None) -> None:
        if   type(include) not in [str, list] and include is not None: raise FilterError("type of parameter include MUST be str, list or None.")
        elif type(exclude) not in [str, list] and exclude is not None: raise FilterError("type of parameter exclude MUST be str, list or None.")
        self.incl = [include] if type(include) == str else include
        self.excl = [exclude] if type(exclude) == str else exclude

    def _preprocess_pattern(self, pattern: str) -> str:
        escaped_pattern = re.escape(pattern)
        processed_pattern = escaped_pattern.replace(r"\*", ".*")
        return "^" + processed_pattern + "$"
    
    def matches_pattern(self, pattern: str, dest: str) -> bool:
        return bool(re.search(self._preprocess_pattern(pattern), dest))

    def matches_patterns(self, pattern: List[str], dest: str) -> bool:
        for pat in pattern:
            if self.matches_pattern(pat, dest): return pat
        return False