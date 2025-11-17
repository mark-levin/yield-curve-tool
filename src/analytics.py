import pandas as pd


def compute_spreads(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute curve metrics like 2s10s, 5s30s.
    Expects a long DataFrame with ['date', 'tenor_years', 'yield'].
    """
    pivot = df.pivot_table(
        index="date",
        columns="tenor_years",
        values="yield",
    )
    
    pivot = pivot.rename(columns={
        2.0: "y2",
        5.0: "y5",
        10.0: "y10",
        30.0: "y30",
    })

    out = pd.DataFrame(index=pivot.index)
    if {"y2", "y10"}.issubset(pivot.columns):
        out["slope_2s10s"] = pivot["y10"] - pivot["y2"]
    if {"y5", "y30"}.issubset(pivot.columns):
        out["slope_5s30s"] = pivot["y30"] - pivot["y5"]

    out = out.dropna(how="all")
    return out.reset_index()
