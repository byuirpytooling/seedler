from random import Random

class Sprout:
    def __init__(self, seed):
        self.__buds = dict()
        self.__rnd: Random = Random(seed)

    def add_bud(self, bud: str, count: int = 1) -> None:
        """
        Adds buds to the sprout.
        Args:
            bud: Bud name to add
            count: How many buds to add. If less than zero buds will not be added.

        Returns: None

        """
        if count < 0:
            return

        if bud not in self.__buds:
            self.__buds[bud] = count
        else:
            self.__buds[bud] += count

    def growth(self, a: int, b: int) -> int:
        """
        Returns a random integer between a and b.
        Args:
            a: value one
            b: value 2

        Returns: random number from range [a,b]

        """
        return self.__rnd.randint(a, b)

    def get_count(self, name: str) -> int:
        """
        Returns the count of ``name`` in the sprout.
        Args:
            name: Bud name to count

        Returns: int count of bud ``name``, 0 if not found

        """
        if not name in self.__buds:
            return 0

        return self.__buds[name]