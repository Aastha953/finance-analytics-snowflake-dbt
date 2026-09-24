import pandas as pd
from pathlib import Path
from faker import Faker
import random


# ---------------------------------------------------------
# PROJECT SETUP
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

fake = Faker()

# Reproducible data
Faker.seed(42)
random.seed(42)


# ---------------------------------------------------------
# VENDOR DATA
# ---------------------------------------------------------

vendor_categories = [
    "Technology",
    "Facilities",
    "Professional Services",
    "Marketing",
    "Office Supplies",
    "Transportation",
    "Raw Materials",
    "Utilities",
    "Equipment",
    "Consulting"
]

states = [
    "CT",
    "MA",
    "NY",
    "NJ",
    "PA",
    "VA",
    "NC",
    "GA",
    "TX",
    "CA",
    "IL",
    "OH",
    "MI",
    "FL",
    "CO"
]


vendors = []


for i in range(1, 101):

    vendor = {
        "vendor_id": f"VEND{i:04d}",

        "vendor_name": fake.company(),

        "vendor_category": random.choice(
            vendor_categories
        ),

        "city": fake.city(),

        "state": random.choice(states),

        "payment_terms": random.choice([
            "NET15",
            "NET30",
            "NET45",
            "NET60"
        ])
    }

    vendors.append(vendor)


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(vendors)


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

output_file = DATA_DIR / "vendors.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Vendors created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print(df.head(10).to_string(index=False))