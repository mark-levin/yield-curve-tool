# Yield Curve Tool

  

Command-line workflow for downloading, storing, and visualizing the U.S. Treasury yield curve. The tool talks to the [FRED](https://fred.stlouisfed.org/) API, writes the data to a local SQLite database, and offers quick analytics/plots such as curve levels and 2s10s or 5s30s spreads.

  

## Configuration

The CLI expects the API key in the environment variable `FRED_API_KEY` (free; create an account at fred.stlouisfed.org). You can place it in a `.env` file at the repo root (loaded via `python-dotenv`).

You can also optionally override the default database location. If not specified, the CLI uses `sqlite:///yield_curves.db`.  

```env
FRED_API_KEY=your-key-here
DB_URL=sqlite:///yield_curves.db
```

  

## Usage

The entry point is `src/cli.py`. Run it with `python -m src.cli <command> [options]`.

  

### Download historical curves

```bash

python -m src.cli download --start 2018-01-01 --end 2024-01-01

```

Downloads all configured tenors for the date range and writes them to `yield_curves.db`. Re-running with overlapping dates updates (upserts) existing rows.

  

### Plot a curve for specific dates

```bash

python -m src.cli plot-curve --dates 2020-03-10 2023-05-01

```

Loads stored data and overlays each requested date on a single chart. 

  

### Plot spreads through time

```bash

python -m src.cli plot-spreads

```

Computes 2s10s and 5s30s from the stored series and produces a timeseries plot.

  

## Data storage

- Default DB: `sqlite:///yield_curves.db` in the project root.

- Table: `yield_curve_points` with columns `date`, `curve_name`, `tenor_years`, `yield_value`.

- Primary key format: `<date>_<curve_name>_<tenor>`.

  

To inspect the database manually you can use any SQLite browser or the `sqlite3` CLI:

  

```bash

sqlite3 yield_curves.db "SELECT date, tenor_years, yield_value FROM yield_curve_points LIMIT 5;"

```

  
