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

entities = pd.read_csv(
    DATA_DIR / "entities.csv"
)


# ---------------------------------------------------------
# SELECT ACCOUNTS USED FOR P&L
# ---------------------------------------------------------

pl_accounts = chart_of_accounts[
    chart_of_accounts["financial_statement"]
    == "Income Statement"
].copy()


account_ids = pl_accounts["account_id"].tolist()

cost_center_ids = (
    cost_centers["cost_center_id"].tolist()
)

entity_ids = (
    entities["entity_id"].tolist()
)


# ---------------------------------------------------------
# DATE RANGE
# ---------------------------------------------------------

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-09-01")


# ---------------------------------------------------------
# GENERATE GL TRANSACTIONS
# ---------------------------------------------------------

gl_records = []

number_of_transactions = 30000


for i in range(1, number_of_transactions + 1):

    transaction_date = (
        start_date
        + pd.Timedelta(
            days=random.randint(
                0,
                (end_date - start_date).days
            )
        )
    )

    account_id = random.choice(
        account_ids
    )

    account_type = pl_accounts.loc[
        pl_accounts["account_id"] == account_id,
        "account_type"
    ].iloc[0]


    # Generate transaction amount
    amount = round(
        np.random.lognormal(
            mean=7.0,
            sigma=1.0
        ),
        2
    )


    # -----------------------------------------------------
    # DEBIT / CREDIT LOGIC
    # -----------------------------------------------------

    if account_type in [
        "COGS",
        "Operating Expense",
        "Other Expense"
    ]:

        debit = amount
        credit = 0.0

    elif account_type in [
        "Revenue",
        "Other Income"
    ]:

        debit = 0.0
        credit = amount

    else:

        debit = 0.0
        credit = 0.0


    gl_records.append({

        "transaction_id":
            f"GL{i:08d}",

        "transaction_date":
            transaction_date.date(),

        "account_id":
            account_id,

        "cost_center_id":
            random.choice(cost_center_ids),

        "entity_id":
            random.choice(entity_ids),

        "debit":
            debit,

        "credit":
            credit,

        "currency":
            "USD",

        "description":
            random.choice([
                "Monthly operating expense",
                "Customer revenue",
                "Material purchase",
                "Payroll expense",
                "Marketing expense",
                "Technology expense",
                "Professional services",
                "Manufacturing cost",
                "Sales transaction",
                "Month-end journal"
            ]),

        "source_system":
            random.choice([
                "ERP",
                "Manual Journal",
                "AP",
                "AR",
                "Payroll"
            ])
    })


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(gl_records)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "general_ledger.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("General Ledger created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print("Total Debits:")
print(
    f"${df['debit'].sum():,.2f}"
)

print()

print("Total Credits:")
print(
    f"${df['credit'].sum():,.2f}"
)

print()

print("Transactions by Source System:")
print(
    df["source_system"].value_counts()
)

print()

print(
    df.head(10).to_string(index=False)
)