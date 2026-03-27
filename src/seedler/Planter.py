import pandas as pd
from .Sprout import Sprout

class Planter(object):
    def __init__(self):
        self.df = pd.DataFrame({
            'seed': pd.Series(dtype="int"),
            'results': pd.Series(dtype="object"),
        })

    def add_seed(self, sprout: Sprout):
        self.df.loc[len(self.df)] = [sprout.seed, sprout.results()]

    def expanded_results(self) -> pd.DataFrame:
        results_expanded = self.df["results"].apply(pd.Series)
        df_pivot = pd.concat([self.df["seed"], results_expanded], axis = 1)
        df_pivot = df_pivot.fillna(0).astype(int)

        return df_pivot