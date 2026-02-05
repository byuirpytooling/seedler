from abc import ABC, abstractmethod
from Sprout import Sprout
from Flamethrower import Flamethrower

class PlanterLab(ABC):
    def __init__(self):
        self.sprout : Sprout | None = None

    @abstractmethod
    def __plant(self) -> None:
        """
        Defines a seeds test. Assign conditions inside with ``self.sprout.add_bud("COND_NAME")``
        Returns: None

        """
        # to be overridden
        pass

    def find_seeds(self, flamethrower: Flamethrower, minimum: int = 0, maximum: int = 100_000) -> None:   # TODO return a Planter
        """
        Finds all matching seeds within range that pass the purging conditions
        Args:
            flamethrower: Flamethrower object for seed purging
            minimum: Starting seeds testing number
            maximum: Ending seeds testing number
        Returns: None

        """
        found_seeds = []

        for i in range(min(minimum, maximum), max(maximum, minimum), 1):
            # get sprout
            self.sprout = Sprout(i)
            # run test
            self.__plant()

            # purge on conditions
            if flamethrower.purge(self.sprout):
                continue

            found_seeds.append(i)

        # reset all temp vars
        flamethrower.reset()
        self.sprout = None

        # return found seeds
        print("FOUND SEEDS: ", ','.join(found_seeds))