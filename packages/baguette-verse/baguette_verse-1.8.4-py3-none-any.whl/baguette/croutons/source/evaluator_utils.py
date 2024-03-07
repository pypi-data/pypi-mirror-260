"""
This module contains a set of objects that are made available in the context of Evaluator code.
As such any value defined in this module is accessible in any Evaluator expression.
"""

from typing import Any

__all__ = ["RE"]





class RE:

    """
    A wrapper for the Pattern class of the re module that have practical syntax usage instead of methods.
    """

    from re import compile
    __compile = staticmethod(compile)
    del compile

    def __init__(self, pattern : str) -> None:
        if not isinstance(pattern, str):
            raise TypeError(f"Expected str, got '{type(pattern).__name__}'")
        self.pattern = RE.__compile(pattern)
    
    def __eq__(self, string : Any) -> bool:
        """
        Implements self == string.
        Returns True if the string is a full match of the expression.
        """
        if isinstance(string, RE):
            return self.pattern == string.pattern
        elif isinstance(string, str):
            return bool(self.pattern.fullmatch(string))
        else:
            return False

    def __le__(self, string : str) -> bool:
        """
        Implements self <= string.
        Returns True if the string contains the expression.
        """
        if not isinstance(string, str):
            return NotImplemented
        return bool(self.pattern.search(string))

    def __lt__(self, string : str) -> bool:
        """
        Implements self < string.
        Returns True if the string contains the expression but is not a full match.
        """
        if not isinstance(string, str):
            return NotImplemented
        return bool((match := self.pattern.search(string)) and len(match.group(0)) < len(string))





del Any