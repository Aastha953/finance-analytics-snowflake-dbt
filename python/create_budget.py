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
# LOAD MASTER DATA
# ---------------------------------------------------------

chart_of_accounts = pd.read_csv(
    DATA_DIR / "chart_of_accounts.csv"
)

cost_centers = pd.read_csv(
    DATA_DIR / "cost_centers.csv"
)


# ---------------------------------------------------------
# SELECT BUDGETABLE ACCOUNTS
# ---------------------------------------------------------

budget_accounts = chart_of_accounts[
    chart_of_accounts["account_type"].isin([
        "COGS",
        "Operating Expense"
    ])
].copy()


account_ids = budget_accounts[
    "account_id"
].tolist()

cost_center_ids = cost_centers[
    "cost_center_id"
].tolist()


# ---------------------------------------------------------
# MONTHS
# ---------------------------------------------------------

months = pd.date_range(
    start="2024-01-01",
    end="2026-09-01",
    freq="MS"
)


# ---------------------------------------------------------
# GENERATE BUDGET
# ---------------------------------------------------------

budget_records = []


for month in months:

    for account_id in account_ids:

        for cost_center_id in cost_center_ids:

            budget_amount = round(
                np.random.uniform(
                    10000,
                    100000
                ),
                2
            )

            budget_records.append({

                "budget_month":
                    month.date(),

                "account_id":
                    account_id,

                "cost_center_id":
                    cost_center_id,

                "budget_amount":
                    budget_amount
            })


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(
    budget_records
)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "budget.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Budget data created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print("Total Budget:")
print(
    f"${df['budget_amount'].sum():,.2f}"
)

print()

print("Budget by Year:")

df["year"] = pd.to_datetime(
    df["budget_month"]
).dt.year

print(
    df.groupby("year")[
        "budget_amount"
    ].sum()
)

print()

print(
    df.head(10).to_string(
        index=False
    )
)