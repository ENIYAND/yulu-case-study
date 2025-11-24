"""
src/data_processing.py

Load, clean and feature-engineer the Bike Sharing dataset used in your notebook.

"""

from pathlib import Path
import pandas as pd
import numpy as np
import argparse

DEFAULT_URL = "https://d2beiqkhq929f0.cloudfront.net/public_assets/assets/000/001/428/original/bike_sharing.csv?1642089089"
DEFAULT_INPUT = Path("data/yulu_data.csv")
DEFAULT_OUTPUT = Path("data/processed_yulu_data.csv")


def load_data(path: str = None, url: str = None) -> pd.DataFrame:
    """Load CSV either from a local path or a URL."""
    if url:
        df = pd.read_csv(url)
        print(f"[load_data] Loaded data from URL: {url}")
    elif path:
        df = pd.read_csv(path)
        print(f"[load_data] Loaded data from file: {path}")
    else:
        if DEFAULT_INPUT.exists():
            df = pd.read_csv(DEFAULT_INPUT)
            print(f"[load_data] Loaded data from default path: {DEFAULT_INPUT}")
        else:
            df = pd.read_csv(DEFAULT_URL)
            print(f"[load_data] No local file - loaded data from default URL.")
    return df


def basic_clean(df: pd.DataFrame) -> pd.DataFrame:
    """Standard cleaning: lowercase columns, parse datetime, drop duplicates."""
    df = df.rename(columns=lambda c: c.strip().lower())
    # parse datetime
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    # drop exact duplicates
    df = df.drop_duplicates().reset_index(drop=True)
    return df


def impute_and_cast(df: pd.DataFrame) -> pd.DataFrame:
    """Cast numeric columns and impute missing with medians (where sensible)."""
    numeric_cols = ["temp", "atemp", "humidity", "windspeed", "casual", "registered", "count"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            med = df[c].median()
            if np.isnan(med):
                med = 0
            df[c] = df[c].fillna(med)

    # cast season/weather/workingday to int if present
    for c in ["season", "weather", "workingday", "holiday"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)
    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Create time-based features and categories similar to notebook."""
    if "datetime" in df.columns:
        df["hour"] = df["datetime"].dt.hour
        df["day_of_week"] = df["datetime"].dt.day_name()
        df["weekday"] = df["datetime"].dt.weekday  # Monday=0
        df["month"] = df["datetime"].dt.month
        df["year"] = df["datetime"].dt.year

        # helpful date-only column for grouping in some notebook cells
        df["date"] = df["datetime"].dt.date

    # season_label mapping seen in notebook
    if "season" in df.columns:
        season_map = {1: "spring", 2: "summer", 3: "fall", 4: "winter"}
        df["season_label"] = df["season"].map(season_map).fillna("unknown")

    # weather label mapping (common mapping)
    if "weather" in df.columns:
        weather_map = {1: "clear", 2: "mist/cloudy", 3: "light_precip", 4: "heavy_precip"}
        df["weather_label"] = df["weather"].map(weather_map).fillna("unknown")

    # If count missing, compute from registered+casual if available
    if "count" not in df.columns and {"registered", "casual"}.issubset(df.columns):
        df["count"] = df["registered"] + df["casual"]

  
    # Temperature categories: use quantiles for ~even bins (adjust as needed)
    if "temp" in df.columns and "temp_category" not in df.columns:
        df["temp_category"] = pd.qcut(df["temp"], q=4, labels=["cold", "mild", "warm", "hot"])

    if "atemp" in df.columns and "atemp_category" not in df.columns:
        df["atemp_category"] = pd.qcut(df["atemp"], q=4, labels=["cold", "mild", "warm", "hot"])

    if "humidity" in df.columns and "humidity_category" not in df.columns:
        df["humidity_category"] = pd.cut(df["humidity"], bins=[-1, 30, 60, 100], labels=["low", "medium", "high"])

    if "windspeed" in df.columns and "windspeed_category" not in df.columns:
        # small nonzero floor to avoid identical values causing single bin
        df["windspeed"] = df["windspeed"].replace(0, df["windspeed"].median())
        df["windspeed_category"] = pd.qcut(df["windspeed"], q=3, labels=["low", "medium", "high"])

    return df


def process(input_path: str = None, url: str = None, output_path: str = None) -> pd.DataFrame:
    """Run the full pipeline and save processed CSV."""
    output_path = Path(output_path) if output_path else DEFAULT_OUTPUT
    df = load_data(path=input_path, url=url)
    df = basic_clean(df)
    df = impute_and_cast(df)
    df = feature_engineering(df)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[process] Wrote processed CSV: {output_path}")
    print("[process] Columns:", list(df.columns))
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Yulu / Bike-sharing dataset")
    parser.add_argument("--input", "-i", help="Local CSV path (e.g. data/yulu_data.csv)")
    parser.add_argument("--url", "-u", help="CSV download URL")
    parser.add_argument("--output", "-o", default=str(DEFAULT_OUTPUT), help="Output processed CSV path")
    args = parser.parse_args()
    process(input_path=args.input, url=args.url, output_path=args.output)
