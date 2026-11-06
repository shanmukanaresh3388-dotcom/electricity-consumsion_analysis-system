"""
Electricity Consumption Analysis System
Intermediate Python mini-project
Uses pandas and matplotlib. No special hardware required.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "electricity_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

UNIT_RATE = 6.0  # Example rate in INR per kWh; change to suit your assignment.


def load_data():
    """Load and validate electricity consumption records."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}\n"
            "Make sure data/electricity_data.csv exists."
        )
    df = pd.read_csv(DATA_FILE)
    required = {"Month", "Units_kWh"}
    if not required.issubset(df.columns):
        raise ValueError("CSV must contain Month and Units_kWh columns.")
    df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m", errors="coerce")
    df["Units_kWh"] = pd.to_numeric(df["Units_kWh"], errors="coerce")
    df = df.dropna(subset=["Month", "Units_kWh"])
    df = df[df["Units_kWh"] >= 0].copy()
    if df.empty:
        raise ValueError("No valid records found in the dataset.")
    df = df.sort_values("Month").drop_duplicates(subset=["Month"], keep="last")
    df["Estimated_Bill_INR"] = df["Units_kWh"] * UNIT_RATE
    df["Month_Name"] = df["Month"].dt.strftime("%b %Y")
    return df


def print_summary(df):
    """Print key statistics to the terminal."""
    total_units = df["Units_kWh"].sum()
    average_units = df["Units_kWh"].mean()
    highest = df.loc[df["Units_kWh"].idxmax()]
    lowest = df.loc[df["Units_kWh"].idxmin()]
    total_bill = df["Estimated_Bill_INR"].sum()

    print("\n" + "=" * 58)
    print("       ELECTRICITY CONSUMPTION ANALYSIS SYSTEM")
    print("=" * 58)
    print(f"Records analysed       : {len(df)} months")
    print(f"Total consumption      : {total_units:,.1f} kWh")
    print(f"Average monthly usage  : {average_units:,.1f} kWh")
    print(f"Estimated total bill   : Rs. {total_bill:,.2f}")
    print(f"Highest consumption   : {highest['Month_Name']} ({highest['Units_kWh']:.1f} kWh)")
    print(f"Lowest consumption    : {lowest['Month_Name']} ({lowest['Units_kWh']:.1f} kWh)")
    print(f"Assumed rate           : Rs. {UNIT_RATE:.2f} per kWh")
    print("-" * 58)
    print(df[["Month_Name", "Units_kWh", "Estimated_Bill_INR"]].to_string(
        index=False,
        formatters={
            "Units_kWh": lambda x: f"{x:.1f}",
            "Estimated_Bill_INR": lambda x: f"Rs. {x:,.2f}"
        }
    ))
    print("=" * 58)


def create_charts(df):
    """Create a consumption bar chart and a consumption trend line chart."""
    labels = df["Month"].dt.strftime("%b")
    units = df["Units_kWh"]

    # Chart 1: monthly consumption
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar(labels, units)
    ax.set_title("Monthly Electricity Consumption")
    ax.set_xlabel("Month")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    for bar, value in zip(bars, units):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{value:.0f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    bar_path = OUTPUT_DIR / "monthly_consumption_bar_chart.png"
    fig.savefig(bar_path, dpi=160)
    plt.show()
    plt.close(fig)

    # Chart 2: consumption trend
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.plot(df["Month"], units, marker="o", linewidth=2)
    ax.set_title("Electricity Consumption Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(True, linestyle="--", alpha=0.35)
    fig.autofmt_xdate()
    fig.tight_layout()
    line_path = OUTPUT_DIR / "consumption_trend_line_chart.png"
    fig.savefig(line_path, dpi=160)
    plt.show()
    plt.close(fig)

    # Chart 3: estimated bill
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bill_values = df["Estimated_Bill_INR"]
    bars = ax.bar(labels, bill_values)
    ax.set_title(f"Estimated Monthly Electricity Bill (Rs. {UNIT_RATE:.2f}/kWh)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Estimated bill (INR)")
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    for bar, value in zip(bars, bill_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{value:.0f}", ha="center", va="bottom", fontsize=8)
    fig.tight_layout()
    bill_path = OUTPUT_DIR / "estimated_monthly_bill_chart.png"
    fig.savefig(bill_path, dpi=160)
    plt.show()
    plt.close(fig)

    print("\nCharts saved to:")
    print(f" - {bar_path}")
    print(f" - {line_path}")
    print(f" - {bill_path}")


def export_analysis(df):
    """Save the processed data with estimated bills to a new CSV file."""
    export_columns = ["Month_Name", "Units_kWh", "Estimated_Bill_INR"]
    export_df = df[export_columns].rename(columns={"Month_Name": "Month"})
    export_path = OUTPUT_DIR / "electricity_analysis_results.csv"
    export_df.to_csv(export_path, index=False)
    print(f"Analysis results saved to: {export_path}")


def main():
    try:
        df = load_data()
        print_summary(df)
        export_analysis(df)
        create_charts(df)
    except (FileNotFoundError, ValueError, pd.errors.ParserError) as exc:
        print(f"\nError: {exc}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
