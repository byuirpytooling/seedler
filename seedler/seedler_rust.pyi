from typing import Dict, Optional, List, Tuple, Any

class Sprout:
    """A high-performance state container for seed simulation.

    The Sprout holds the internal RNG state and a collection of 'buds' (event counts).
    It is designed to be passed between the Planter (logic) and Fire (filter).
    """

    seed: int
    """The u64 seed used to initialize this specific sprout's RNG."""

    def __init__(self, seed: int) -> None:
        """Initializes a new Sprout.

        Args:
            seed (int): The initial u64 seed for deterministic randomness.
        """
        ...

    def reset(self, new_seed: int) -> None:
        """Resets the sprout state to allow memory reuse in tight loops.

        Args:
            new_seed (int): The new seed to re-initialize the PRNG.
        """
        ...

    def add_bud(self, bud_id: int, count: Optional[int] = None) -> None:
        """Registers a count for a specific bud ID.

        Args:
            bud_id (int): A unique identifier for the event/item being tracked.
            count (int, optional): The amount to increment by. Defaults to 1.
        """
        ...

    def get_bud_count(self, bud_id: int) -> int:
        """Retrieves the current count for a bud ID without Python overhead.

        Args:
            bud_id (int): The ID to look up.

        Returns:
            int: The current count, or 0 if the ID has not been added.
        """
        ...

    def growth(self, a: int, b: int) -> int:
        """Generates a random integer within an inclusive range using the internal PRNG.

        Args:
            a (int): Inclusive lower bound.
            b (int): Inclusive upper bound.

        Returns:
            int: A pseudo-random integer.
        """
        ...

    def to_dict(self) -> Dict[int, int]:
        """Exports the internal bud mapping to a Python dictionary.

        Returns:
            dict: A dictionary mapping bud_ids to their respective counts.
        """
        ...

class PlanterLab:
    """The execution engine for batch-processing and filtering sprouts.

    PlanterLab handles the heavy lifting of iterating through seed ranges
    in compiled code while calling back to Python for custom logic.
    """

    def __init__(self) -> None: ...

    def find_seeds(
        self, 
        fire: Optional[Any] = None, 
        minimum: int = 0, 
        maximum: int = 100000
    ) -> List[Tuple[int, Dict[int, int]]]:
        """Orchestrates a search loop across a range of seeds.

        This method iterates from minimum to maximum, creating a Sprout for each
        seed, executing 'plant', and checking the 'fire' filter.

        Args:
            fire (Fire, optional): A filter object with a 'purge' method.
            minimum (int): The starting seed (inclusive).
            maximum (int): The ending seed (exclusive).

        Returns:
            list[tuple[int, dict]]: A list of tuples containing (seed, results_dict).
        """
        ...

    def plant(self, sprout: Sprout) -> None:
        """Interface method for defining bud growth logic.

        Users should subclass PlanterLab and override this method in Python.
        """
        ...