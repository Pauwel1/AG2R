import pandas as pd

def style_df(df: pd.DataFrame, props):
    for val in df["fluctuation"]:
        return props if val == "Down" else None