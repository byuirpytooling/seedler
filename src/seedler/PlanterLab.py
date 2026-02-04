from abc import ABC, abstractmethod
from Sprout import Sprout

class PlanterLab(ABC):
    def __init__(self):
        self.sprout : Sprout | None = None
        self.__prune_calls : list[dict] | None = None

    @abstractmethod
    def __plant(self) -> None:
        """
        Defines a seeds test. Assign conditions inside with ``self.sprout.add_bud("COND_NAME")``
        Returns: None

        """
        # to be overridden
        pass

    @abstractmethod
    def __purge(self) -> None:
        """
        Defines conditions for Sprout purging with self.prune(NAME, VALUE)
        Returns: None

        """
        # to be overridden
        pass

    def prune(self, name: str, value: int) -> None:
        """
        Defines a pruning condition for Sprout
        Args:
            name: Sprout bud to test
            value: Test value

        Returns: None

        """
        self.__prune_calls.append({"name": name, "val": value})    # TODO add Conditional calls

    def __do_purge(self) -> bool:
        """
        Tests if the sprout needs to be purged
        Returns: True iff sprout fails one or more pruning conditions

        """
        for call in self.__prune_calls:
            if self.sprout.get_count(call["name"]) > call["val"]:
                return True

        return False

    def find_seeds(self, minimum: int = 0, maximum: int = 100_000) -> None:   # TODO return a Planter
        """
        Finds all matching seeds within range that pass the purging conditions
        Args:
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

            # reset pruning calls
            self.__prune_calls = []
            # get pruning conditions
            self.__purge()
            # test for pass/fail
            if self.__do_purge():
                continue

            found_seeds.append(i)

        # reset all temp vars
        self.sprout = None
        self.__prune_calls = None

        # return found seeds
        print("FOUND SEEDS: ", ','.join(found_seeds))