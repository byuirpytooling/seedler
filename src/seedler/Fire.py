from abc import ABC, abstractmethod
from .Sprout import Sprout

class Fire(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def _purge(self, sprout: Sprout):
        """
        Defines conditions for Sprout purging with self.prune(NAME, VALUE)
        Args:
            sprout (Sprout): The sprout to test
        Returns: If returns true, purges the seed

        """
        # to be overridden
        pass

    def purge(self, sprout: Sprout) -> bool:
        """
        Tests if the sprout needs to be purged
        Args:
            sprout (Sprout): The sprout to test
        Returns: True iff sprout fails one or more pruning conditions

        """

        return self._purge(sprout)