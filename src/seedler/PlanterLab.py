from abc import ABC, abstractmethod
from .Sprout import Sprout
from .Fire import Fire
from .Planter import Planter

class PlanterLab(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def _plant(self, sprout: Sprout) -> None:
        """
        Defines a seeds test. Assign conditions inside with ``self.sprout.add_bud("COND_NAME")``
        Args:
            sprout (Sprout): Sprout object
        Returns: None

        """
        # to be overridden
        pass

    def find_seeds(self, fire: Fire = None, minimum: int = 0, maximum: int = 100_000) -> Planter:
        """
        Finds all matching seeds within range that pass the purging conditions
        Args:
            fire: Fire object for seed purging
            minimum: Starting seeds testing number
            maximum: Ending seeds testing number
        Returns: Planter

        """
        planter = Planter()

        for i in range(min(minimum, maximum), max(maximum, minimum), 1):
            # get sprout
            sprout = Sprout(i)
            # run test
            self._plant(sprout)

            # purge on conditions
            if fire is not None:
                if fire.purge(sprout):
                    continue

            planter.add_seed(sprout)

        # return found seeds
        return planter