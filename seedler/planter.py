from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Dict
from . import seedler_rust as _core
from .fire import Fire

class Planter(_core.PlanterLab, ABC):
    """
    Main entry point for seed simulations.

    Inherit from this class and override the `plant` method to define
    how your sprouts evolve buds.
    """

    @abstractmethod
    def plant(self, sprout: _core.Sprout):
        """
        Defines the evolution logic for a single sprout.

        Args:
            sprout: The sprout instance to modify.
        """
        pass

    def find_seeds(
        self, 
        fire: Optional[Fire] = None, 
        minimum: int = 0, 
        maximum: int = 100_000
    ) -> List[Tuple[int, Dict[int, int]]]:
        """
        Executes a high-speed search across a range of seeds.

        Args:
            fire: An optional filter object with a `purge` method.
            minimum: Starting seed index.
            maximum: Ending seed index.

        Returns:
            A list of tuples containing the valid seed and its bud results.
        """
        return super().find_seeds(fire, minimum, maximum)