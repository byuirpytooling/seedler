from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import seedler_rust

class Fire(ABC):
    """
    Base class for seed filtering logic.

    Subclass this and implement the `purge` method to filter
    results inside the Rust execution loop.
    """

    @abstractmethod
    def purge(self, sprout: seedler_rust.Sprout) -> bool:
        """
        Criteria for discarding a sprout result.

        Args:
            sprout: The current sprout state.

        Returns:
            True if the sprout should be excluded, False to keep it.
        """
        return False