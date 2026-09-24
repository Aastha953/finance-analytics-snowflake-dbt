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
# DATE RANGE
# ---------------------------------------------------------

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-09-01")


# ---------------------------------------------------------
# GENERATE AR INVOICES
# ---------------------------------------------------------

ar_records = []

number_of_invoices = 5000


for i in range(1, number_of_invoices + 1):

    invoice_date = start_date + pd.Timedelta(
        days=random.randint(
            0,
            (end_date - start_date).days
        )
    )

    payment_terms = random.choice([
        15,
        30,
        45,
        60
    ])

    due_date = invoice_date + pd.Timedelta(
        days=payment_terms
    )

    invoice_amount = round(
        np.random.lognormal(
            mean=7.5,
            sigma=0.9
        ),
        2
    )

    # Around 80% of invoices are eventually paid
    is_paid = random.random() > 0.20

    payment_date = None
    payment_amount = 0.0

    if is_paid:

        payment_delay = random.randint(
            -15,
            60
        )

        payment_date = due_date + pd.Timedelta(
            days=payment_delay
        )

        # Don't allow payment after our dataset end date
        if payment_date <= end_date:

            payment_amount = invoice_amount

        else:

            payment_date = None
            payment_amount = 0.0

    status = (
        "PAID"
        if payment_date is not None
        else "OPEN"
    )

    ar_records.append({

        "invoice_id":
            f"AR{i:06d}",

        "customer_id":
            random.choice(customer_ids),

        "invoice_date":
            invoice_date.date(),

        "due_date":
            due_date.date(),

        "payment_date":
            (
                payment_date.date()
                if payment_date is not None
                else None
            ),

        "invoice_amount":
            invoice_amount,

        "payment_amount":
            payment_amount,

        "currency":
            "USD",

        "status":
            status
    })


# ---------------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------------

df = pd.DataFrame(ar_records)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "accounts_receivable.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Accounts Receivable data created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()

print("Total Invoice Amount:")
print(
    f"${df['invoice_amount'].sum():,.2f}"
)

print()

print("Total Payment Amount:")
print(
    f"${df['payment_amount'].sum():,.2f}"
)

print()

print("Outstanding AR:")

outstanding = (
    df["invoice_amount"].sum()
    -
    df["payment_amount"].sum()
)

print(
    f"${outstanding:,.2f}"
)

print()

print("Invoice Status:")
print(
    df["status"].value_counts()
)

print()

print(
    df.head(10).to_string(index=False)
)