from __future__ import annotations
from typing import Optional, Dict
from . import seedler_rust

class Sprout:
    """
    A high-performance container for bud data and random growth logic.

    This class wraps a Rust-based Sprout object to ensure maximum execution 
    speed during heavy simulation loops.

    Attributes:
        seed (int): The unique seed value used to initialize the RNG.
    """

    def __init__(self, seed: int):
        """
        Initializes a new Sprout.

        Args:
            seed: The numerical seed for random number generation.
        """
        self._raw = seedler_rust.Sprout(seed)

    @property
    def seed(self) -> int:
        """Returns the current seed of the sprout."""
        return self._raw.seed

    def add_bud(self, name: int, count: Optional[int] = 1):
        """
        Adds a named bud to the collection.

        Args:
            name: The identifier for the bud.
            count: How many units to add. Defaults to 1.
        """
        self._raw.add_bud(name, count)

    def growth(self, a: int, b: int) -> int:
        """
        Generates a random growth factor using the internal Rust PRNG.

        Args:
            a: The lower inclusive bound.
            b: The upper inclusive bound.

        Returns:
            A random integer between a and b.
        """
        return self._raw.growth(a, b)

    def to_dict(self) -> Dict[int, int]:
        """
        Converts the internal bud collection to a Python dictionary.

        Returns:
            A dictionary of bud names and their counts.
        """
        return self._raw.to_dict()
    
    def get_bud_count(self, key: int) -> int:
        """
        Gets the count of a specific bud on the sprout.

        Returns:
            The integer count of the bud on the sprout.
        """

        return self._raw.get_bud_count(key)