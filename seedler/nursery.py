import pandas as pd
from typing import List, Tuple, Dict

class Nursery:
    """
    Static class to convert `Planter` results (sprouts raw) into a dataframe.
    """

    @staticmethod
    def pandas(data: List[Tuple[int, Dict[int, int]]], expanded=False) -> pd.DataFrame:
        """
        Converts planter sprout results into a pandas DataFrame.

        Args:
            data: List of raw sprout data from Planter.find_seeds()

        Returns:
            pandas.DataFrame
        """
        
        raw = {"Seed": [], "Data": []}

        for line in data:
            seed = line[0]
            d = line[1]
            raw["Seed"].append(seed)
            raw["Data"].append(d)
        
        df = pd.DataFrame(raw)

        if expanded:
            expanded_df = df['Data'].apply(pd.Series)
            return pd.concat([df['Seed'], expanded_df], axis=1).fillna(0).astype(int)

        return df