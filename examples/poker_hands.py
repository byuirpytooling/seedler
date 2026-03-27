from seedler.PlanterLab import PlanterLab
from seedler.Fire import Fire
from seedler.Sprout import Sprout

suits = ["H", 'S', 'D', 'C']
values = ["A", "K", "Q", "J", '10', '9', '8', '7', '6', '5', '4', '3', '2']

base_deck = [f"{val}{suit}" for suit in suits for val in values]

class PokerLab(PlanterLab):
    def __flush(self, hand):
        suit = hand[0][-1]

        for c in hand:
            if c[-1] != suit:
                return False

        return True

    def __straight(self, hand):
        vals = []
        ace = False
        for c in hand:
            val = c[:-1]

            if val == "A":
                if ace:
                    return False
                ace = True
                continue

            if val == "K": val = 13
            elif val == "Q": val = 12
            elif val == "J": val = 11
            else: val = int(val)

            vals.append(val)

        if ace:
            if 13 in vals: vals.append(14)
            else: vals.append(1)

        if max(vals) - min(vals) != 4: return False
        if len(set(vals)) != 5: return False

        return True

    def __max_kind(self, hand):
        counts = {}
        for c in hand:
            if c not in counts: counts[c] = 0
            counts[c] += 1

        return max(counts.values())

    def __values(self, hand):
        vals = []
        for c in hand:
            vals.append(c[:-1])
        return vals

    def _plant(self, sprout: Sprout):
        deck = base_deck.copy()
        hand = []
        for _ in range(5):
            card = deck.pop(sprout.growth(0, len(deck) - 1))
            hand.append(card)

        flush = self.__flush(hand)
        straight = self.__straight(hand)
        max_kind = self.__max_kind(hand)

        vals = self.__values(hand)

        if straight and flush:
            if "A" in vals and "10" in vals:
                sprout.add_bud("royal flush")
                return

            sprout.add_bud("straight flush")
            return

        if max_kind == 4:
            sprout.add_bud("four kind")
            return

        if max_kind == 3 and len(set(vals)) == 2:
            sprout.add_bud("full house")
            return

        if flush:
            sprout.add_bud("flush")
            return

        if straight:
            sprout.add_bud("straight")
            return

        if max_kind == 3:
            sprout.add_bud("three kind")
            return

        if max_kind == 2 and len(set(vals)) == 3:
            sprout.add_bud("two pair")
            return

        if max_kind == 2:
            sprout.add_bud("two kind")
            return

        sprout.add_bud("high card")
        return

class PokerFire(Fire):
    def _purge(self, sprout: Sprout):
        return sprout.get_count("two kind") == 0


lab = PokerLab()
planter = lab.find_seeds(fire=None, minimum=0, maximum=1_000)

print(planter.df)