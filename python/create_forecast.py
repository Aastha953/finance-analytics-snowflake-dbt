import pandas as pd
import numpy as np
from pathlib import Path
import random


# ---------------------------------------------------------
# PROJECT SETUP
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)
np.random.seed(42)


# ---------------------------------------------------------
# LOAD BUDGET
# ---------------------------------------------------------

budget_file = DATA_DIR / "budget.csv"

budget = pd.read_csv(
    budget_file
)


# ---------------------------------------------------------
# CREATE FORECAST
# ---------------------------------------------------------

forecast = budget.copy()


# Forecast is based on budget but adjusted
# to represent updated management expectations.

forecast["forecast_amount"] = (
    forecast["budget_amount"]
    *
    np.random.uniform(
        0.90,
        1.15,
        size=len(forecast)
    )
).round(2)


# ---------------------------------------------------------
# FORECAST VERSION
# ---------------------------------------------------------

forecast["forecast_version"] = "BASELINE"


# Remove budget amount because it belongs
# to the budget table.

forecast = forecast.drop(
    columns=["budget_amount"]
)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "forecast.csv"

forecast.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Forecast data created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(forecast)}")
print()

print("Total Forecast:")
print(
    f"${forecast['forecast_amount'].sum():,.2f}"
)

print()

print("Forecast Versions:")
print(
    forecast["forecast_version"].value_counts()
)

print()

print(
    forecast.head(10).to_string(
        index=False
    )
)