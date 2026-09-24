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
# LOAD CUSTOMERS
# ---------------------------------------------------------

customers_file = DATA_DIR / "customers.csv"

customers = pd.read_csv(customers_file)

customer_ids = customers["customer_id"].tolist()


# ---------------------------------------------------------
# SALES PARAMETERS
# ---------------------------------------------------------

products = [
    "Industrial Equipment",
    "Manufacturing Components",
    "Packaging Materials",
    "Safety Equipment",
    "Maintenance Supplies",
    "Technology Hardware",
    "Office Equipment",
    "Professional Services"
]

business_units = [
    "Manufacturing",
    "Distribution",
    "Services"
]

regions = [
    "Northeast",
    "Southeast",
    "Midwest",
    "Southwest",
    "West"
]


# ---------------------------------------------------------
# GENERATE SALES
# ---------------------------------------------------------

sales = []

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-09-01")

number_of_transactions = 10000


for i in range(1, number_of_transactions + 1):

    sales_date = start_date + pd.Timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    revenue = round(
        np.random.lognormal(
            mean=7.5,
            sigma=0.6
        ),
        2
    )

    cost = round(
        revenue * random.uniform(0.45, 0.75),
        2
    )

    gross_profit = round(
        revenue - cost,
        2
    )

    sales.append({
        "sales_id": f"SALE{i:07d}",

        "sales_date": sales_date.date(),

        "customer_id": random.choice(
            customer_ids
        ),

        "product": random.choice(
            products
        ),

        "business_unit": random.choice(
            business_units
        ),

        "region": random.choice(
            regions
        ),

        "revenue": revenue,

        "cost": cost,

        "gross_profit": gross_profit
    })


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(sales)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "sales.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Sales data created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print("Total Revenue:")
print(f"${df['revenue'].sum():,.2f}")

print()

print("Total Cost:")
print(f"${df['cost'].sum():,.2f}")

print()

print("Gross Profit:")
print(f"${df['gross_profit'].sum():,.2f}")

print()

print(df.head(10).to_string(index=False))