from typing import Optional
import matplotlib.pyplot as plt
import pandas as pd


def plot_curve_on_date(
    df: pd.DataFrame,
    date: pd.Timestamp,
    ax: Optional[plt.Axes] = None,
    label: Optional[str] = None,
):
    """
    Plot yield curve for a single date.
    df: long DataFrame with ['date', 'tenor_years', 'yield'].
    """
    if ax is None:
        fig, ax = plt.subplots()

    day_data = df[df["date"] == date].sort_values("tenor_years")
    ax.plot(day_data["tenor_years"], day_data["yield"], marker="o", label=label or date.date())
    ax.set_xlabel("Tenor (years)")
    ax.set_ylabel("Yield")
    ax.set_title("Yield Curve")
    if label:
        ax.legend()
    return ax


def plot_spread_timeseries(spreads_df: pd.DataFrame):
    """
    Plot curve slopes over time: e.g. 2s10s, 5s30s.
    """
    fig, ax = plt.subplots()
    for col in spreads_df.columns:
        if col == "date":
            continue
        ax.plot(spreads_df["date"], spreads_df[col], label=col)
    ax.set_xlabel("Date")
    ax.set_ylabel("Spread (bp or %)")
    ax.set_title("Curve Spreads Over Time")
    ax.legend()
    fig.autofmt_xdate()
    return ax
