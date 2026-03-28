from seedler import Planter, Fire, Sprout

def test_planterlab_counting():
    test_range = 100

    YES = 0
    FAIL = 1

    class CardMontePlanter(Planter):
        def plant(self, sprout: Sprout):
            cards = [YES, FAIL, FAIL]

            for i in range(3):
                sprout.add_bud(cards[i])

    planter = CardMontePlanter()
    res = planter.find_seeds(fire=None, minimum=0, maximum=test_range)

    assert len(res) == test_range

def test_planterlab_test_count():
    test_range = 100

    YES = 0
    FAIL = 1

    class CardMontePlanter(Planter):
        def plant(self, sprout: Sprout):
            cards = [YES, FAIL, FAIL]
            card = cards[sprout.growth(0, 2)]
            sprout.add_bud(card)

    class TruthFire(Fire):
        def purge(self, sprout: Sprout):
            return sprout.get_bud_count(YES) >= 1

    class FailFire(Fire):
        def purge(self, sprout: Sprout):
            return sprout.get_bud_count(FAIL) >= 1

    plantlab = CardMontePlanter()
    planter_truth = plantlab.find_seeds(fire=TruthFire(), minimum=0, maximum=test_range)
    planter_fail = plantlab.find_seeds(fire=FailFire(), minimum=0, maximum=test_range)

    truths = len(planter_truth)
    fails = len(planter_fail)

    assert truths + fails == test_range