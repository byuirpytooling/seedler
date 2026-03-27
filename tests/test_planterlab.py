from seedler.PlanterLab import PlanterLab
from seedler.Sprout import Sprout
from seedler.Fire import Fire

def test_planterlab_counting():
    test_range = 10

    class CardMontePlanter(PlanterLab):
        def _plant(self, sprout: Sprout):
            cards = ['Yes', "Fail", "Fail"]

            for i in range(3):
                sprout.add_bud(cards[i])

    plantlab = CardMontePlanter()
    planter = plantlab.find_seeds(fire=None, minimum=0, maximum=test_range)

    assert len(planter.df) == test_range

def test_planterlab_test_count():
    test_range = 100

    class CardMontePlanter(PlanterLab):
        def _plant(self, sprout: Sprout):
            cards = ['Yes', "Fail", "Fail"]
            card = cards[sprout.growth(0, 2)]
            sprout.add_bud(card)

    class TruthFire(Fire):
        def _purge(self, sprout: Sprout):
            return sprout.get_count("Yes") >= 1

    class FailFire(Fire):
        def _purge(self, sprout: Sprout):
            return sprout.get_count("Fail") >= 1

    plantlab = CardMontePlanter()
    planter_truth = plantlab.find_seeds(fire=TruthFire(), minimum=0, maximum=test_range)
    planter_fail = plantlab.find_seeds(fire=FailFire(), minimum=0, maximum=test_range)

    truths = len(planter_truth.df)
    fails = len(planter_fail.df)

    assert truths + fails == test_range