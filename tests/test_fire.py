from seedler.Fire import Fire
from seedler.Sprout import Sprout

def test_fire():
    class CardFire(Fire):
        def _purge(self, sprout: Sprout):
            return sprout.get_count("Found") < 1

    fire = CardFire()

    sprout1 = Sprout(1)
    sprout1.add_bud("Found", 2)

    sprout2 = Sprout(2)
    sprout2.add_bud("Not Found", 2)

    sprout3 = Sprout(3)
    sprout3.add_bud("Found")
    sprout3.add_bud("Not Found")

    assert not fire.purge(sprout1)
    assert fire.purge(sprout2)
    assert not fire.purge(sprout3)