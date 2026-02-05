from abc import ABC, abstractmethod
from Sprout import Sprout
from Conditions import Condition

class Flamethrower(ABC):
    def __init__(self) -> None:
        self.__prune_calls = []

    @abstractmethod
    def __purge(self) -> bool | None:
        """
        Defines conditions for Sprout purging with self.prune(NAME, VALUE)
        Returns: If returns true, purges the seed

        """
        # to be overridden
        pass

    def prune(self, name: str, condition: Condition, value: int) -> None:
        """
        Defines a pruning condition for Sprout
        Args:
            name: Sprout bud to test
            condition: The Condition function to test the named parameter value vs. value
            value: Compared value

        Returns: None

        """
        self.__prune_calls.append({"name": name, "cond": condition, "val": value})

    def purge(self, sprout: Sprout) -> bool:
        """
        Tests if the sprout needs to be purged
        Args:
            sprout: The sprout to test
        Returns: True iff sprout fails one or more pruning conditions

        """
        self.__prune_calls = []
        if self.__purge() == True:
            return True

        for call in self.__prune_calls:
            if call['cond'](sprout.get_count(call["name"]), call["val"]):
                return True

        return False

    def reset(self) -> None:
        self.__prune_calls = None