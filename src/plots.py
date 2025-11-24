"""
src/plots.py

Usage:
    # generate all plots using the processed CSV created by data_processing.py
    python src/plots.py --input data/processed_yulu_data.csv
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

sns.set(style="whitegrid")
FIG_DIR = Path("figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig, name):
    path = FIG_DIR / name
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    print("[plot] Saved:", path)


def plot_seasonal_trends(df, season_col="season_label", count_col="count"):
    """Boxplot of rentals across seasons (spring/summer/fall/winter)."""
    if season_col not in df.columns:
        print(f"[plot_seasonal_trends] Missing column: {season_col} - skipping")
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=season_col, y=count_col, data=df, ax=ax)
    ax.set_title("Rental Distribution Across Seasons")
    ax.set_xlabel("Season")
    ax.set_ylabel("Count")
    _save(fig, "seasonal_trends.png")


def plot_temp_vs_count(df, temp_col="temp", count_col="count"):
    """Scatter + smooth line for temperature vs rentals."""
    if temp_col not in df.columns:
        print(f"[plot_temp_vs_count] Missing column: {temp_col} - skipping")
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(x=temp_col, y=count_col, data=df, alpha=0.4, ax=ax)
    try:
        sns.regplot(x=temp_col, y=count_col, data=df, scatter=False, lowess=True, ax=ax, ci=None)
    except Exception:
        # fallback: linear regression line
        sns.regplot(x=temp_col, y=count_col, data=df, scatter=False, ax=ax, ci=None)
    ax.set_title("Temperature vs Rentals")
    ax.set_xlabel("Temperature (C)")
    ax.set_ylabel("Count")
    _save(fig, "temp_vs_count.png")


def plot_hourly_pattern(df, hour_col="hour", count_col="count"):
    """Average rentals by hour of day."""
    if hour_col not in df.columns:
        if "datetime" in df.columns:
            df[hour_col] = pd.to_datetime(df["datetime"]).dt.hour
        else:
            print(f"[plot_hourly_pattern] No '{hour_col}' or 'datetime' column - skipping")
            return
    hourly = df.groupby(hour_col)[count_col].mean().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=hour_col, y=count_col, data=hourly, marker="o", ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_title("Average Rentals by Hour")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Average count")
    _save(fig, "hourly_pattern.png")


def plot_category_counts(df, cat_col="temp_category"):
    """Barplot showing counts per category for a chosen category column."""
    if cat_col not in df.columns:
        print(f"[plot_category_counts] Missing column: {cat_col} - skipping")
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    order = df[cat_col].value_counts().index
    sns.countplot(x=cat_col, data=df, order=order, ax=ax)
    ax.set_title(f"Distribution of {cat_col}")
    _save(fig, f"{cat_col}_distribution.png")


def plot_registered_vs_casual(df, reg_col="registered", casual_col="casual"):
    """Pie chart of total registered vs casual share, and timeseries per date if available."""
    if reg_col in df.columns and casual_col in df.columns:
        total_reg = df[reg_col].sum()
        total_cas = df[casual_col].sum()
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie([total_reg, total_cas], labels=["registered", "casual"], autopct="%1.1f%%", startangle=90)
        ax.set_title("Registered vs Casual Share (total)")
        _save(fig, "registered_vs_casual.png")

        if "date" in df.columns:
            ts = df.groupby("date")[[reg_col, casual_col]].sum().reset_index()
            fig2, ax2 = plt.subplots(figsize=(12, 5))
            sns.lineplot(x="date", y=reg_col, data=ts, label="registered", ax=ax2)
            sns.lineplot(x="date", y=casual_col, data=ts, label="casual", ax=ax2)
            ax2.set_title("Registered vs Casual over time (by date)")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Total rides")
            ax2.legend()
            _save(fig2, "registered_vs_casual_timeseries.png")
    else:
        print("[plot_registered_vs_casual] Missing registered/casual columns - skipping")


def plot_correlation_heatmap(df):
    """Heatmap for numeric correlations."""
    num = df.select_dtypes(include="number")
    if num.shape[1] < 2:
        print("[plot_correlation_heatmap] Not enough numeric columns - skipping")
        return
    corr = num.corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_title("Correlation heatmap (numeric features)")
    _save(fig, "correlation_heatmap.png")


def generate_all(input_csv="data/processed_yulu_data.csv"):
    """Load processed CSV and call all plot functions."""
    p = Path(input_csv)
    if not p.exists():
        raise FileNotFoundError(f"Processed CSV not found: {input_csv}. Run src/data_processing.py first.")
    df = pd.read_csv(p, parse_dates=["datetime"])
    # ensure date column if used in notebook
    if "date" not in df.columns and "datetime" in df.columns:
        df["date"] = pd.to_datetime(df["datetime"]).dt.date

    plot_seasonal_trends(df)
    plot_temp_vs_count(df)
    plot_hourly_pattern(df)
    # category plots (temp/atemp/humidity/windspeed) if available
    for cat in ["temp_category", "atemp_category", "humidity_category", "windspeed_category"]:
        if cat in df.columns:
            plot_category_counts(df, cat_col=cat)
    plot_registered_vs_casual(df)
    plot_correlation_heatmap(df)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate plots for YULU case study")
    parser.add_argument("--input", "-i", default="data/processed_yulu_data.csv", help="Processed CSV path")
    args = parser.parse_args()
    generate_all(input_csv=args.input)
