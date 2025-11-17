import argparse

import pandas as pd

from .config import Config
from .curves import download_and_store_ust_curve
from .storage import load_curve_timeseries
from .analytics import compute_spreads
from .plotting import plot_curve_on_date, plot_spread_timeseries
import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Yield curve downloader & visualizer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dl = subparsers.add_parser("download", help="Download and store historical curves")
    dl.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    dl.add_argument("--end", required=True, help="End date YYYY-MM-DD")

    plot_curve = subparsers.add_parser("plot-curve", help="Plot curve for specific dates")
    plot_curve.add_argument("--dates", nargs="+", required=True, help="Dates YYYY-MM-DD")

    plot_sp = subparsers.add_parser("plot-spreads", help="Plot curve spreads over time")

    return parser.parse_args()


def cmd_download(args: argparse.Namespace, config: Config):
    download_and_store_ust_curve(args.start, args.end, config=config)
    print(f"Downloaded and stored curves from {args.start} to {args.end}")


def cmd_plot_curve(args: argparse.Namespace, config: Config):
    df = load_curve_timeseries(config)
    df["date"] = pd.to_datetime(df["date"])
    fig, ax = plt.subplots()
    for d in args.dates:
        date = pd.to_datetime(d)
        plot_curve_on_date(df, date, ax=ax, label=d)
    ax.legend()
    plt.show()


def cmd_plot_spreads(args: argparse.Namespace, config: Config):
    df = load_curve_timeseries(config)
    spreads = compute_spreads(df)
    plot_spread_timeseries(spreads)
    plt.show()


def main():
    args = parse_args()
    config = Config.from_env()

    if args.command == "download":
        cmd_download(args, config)
    elif args.command == "plot-curve":
        cmd_plot_curve(args, config)
    elif args.command == "plot-spreads":
        cmd_plot_spreads(args, config)


if __name__ == "__main__":
    main()
