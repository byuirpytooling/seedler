from typing import Protocol

class Condition(Protocol):
    def __call__(self, a: int, b: int) -> bool: ...

class L:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is less than ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a < b

        """
        return a < b

class LE:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is less than ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a <= b

        """
        return a <= b

class EQ:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is equal to ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a == b

        """
        return a == b

class NE:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is not equal to ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a != b

        """
        return a != b

class G:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is greater than ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a > b

        """
        return a > b

class GE:
    def __call__(self, a: int, b: int) -> bool:
        """
        Returns ``True`` if ``a`` is greater than ``b``
        Args:
            a: param 1
            b: param 2

        Returns: a >= b

        """
        return a >= b