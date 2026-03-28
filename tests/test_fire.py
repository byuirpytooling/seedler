from seedler import Fire
from seedler.seedler_rust import Sprout

def test_fire():
    FOUND = 0
    NOT_FOUND = 1

    class CardFire(Fire):
        def purge(self, sprout):
            return sprout.get_bud_count(FOUND) < 1

    fire = CardFire()

    sprout1 = Sprout(1)
    sprout1.add_bud(FOUND, 2)

    sprout2 = Sprout(2)
    sprout2.add_bud(NOT_FOUND, 2)

    sprout3 = Sprout(3)
    sprout3.add_bud(FOUND)
    sprout3.add_bud(NOT_FOUND)

    assert not fire.purge(sprout1)
    assert fire.purge(sprout2)
    assert not fire.purge(sprout3)