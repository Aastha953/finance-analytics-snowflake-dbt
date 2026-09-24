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

# Make results reproducible
Faker.seed(42)
random.seed(42)


# ---------------------------------------------------------
# CUSTOMER DATA
# ---------------------------------------------------------

customers = []

customer_segments = [
    "Enterprise",
    "Mid-Market",
    "SMB"
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


for i in range(1, 501):

    customer = {
        "customer_id": f"CUST{i:05d}",

        "customer_name": fake.company(),

        "city": fake.city(),

        "state": random.choice(states),

        "customer_segment": random.choice(
            customer_segments
        ),

        "signup_date": fake.date_between(
            start_date="-5y",
            end_date="today"
        )
    }

    customers.append(customer)


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(customers)


# ---------------------------------------------------------
# SAVE CSV
# ---------------------------------------------------------

output_file = DATA_DIR / "customers.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION OUTPUT
# ---------------------------------------------------------

print("Customers created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print(df.head(10).to_string(index=False))