# Electricity Consumption Analysis System

## Overview
An intermediate Python mini-project that reads monthly electricity usage from a CSV file, calculates summary statistics and estimated bills, creates charts, and exports processed results.

## Requirements
- Python 3.10 or later recommended
- pandas
- matplotlib

## Setup
Open a terminal in this project folder and run:

```bash
python -m pip install -r requirements.txt
python electricity_analysis.py
```

On some Windows installations, use `py` instead of `python`:
```bash
py -m pip install -r requirements.txt
py electricity_analysis.py
```

The program prints a summary, opens three charts, and saves the charts and processed CSV in the `output` folder.

## Dataset format
Edit `data/electricity_data.csv`. Keep the column names exactly as shown:

```csv
Month,Units_kWh
2026-01,120
2026-02,150
```

- `Month` must use `YYYY-MM`.
- `Units_kWh` is monthly electricity consumption in kilowatt-hours (units).
- If a month appears more than once, the last occurrence is used.

## Change the estimated rate
Edit `UNIT_RATE = 6.0` near the top of `electricity_analysis.py`. This is an example rate only. Actual electricity bills may include slab rates, fixed charges, taxes, and other adjustments.

## Output files
- `output/monthly_consumption_bar_chart.png`
- `output/consumption_trend_line_chart.png`
- `output/estimated_monthly_bill_chart.png`
- `output/electricity_analysis_results.csv`

## Limitations
This project uses sample monthly data and a single flat per-unit rate. It does not connect to a real smart meter or calculate a legally accurate utility bill.
