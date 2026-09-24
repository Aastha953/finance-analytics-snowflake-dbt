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
# LOAD VENDORS
# ---------------------------------------------------------

vendors_file = DATA_DIR / "vendors.csv"

vendors = pd.read_csv(vendors_file)

vendor_ids = vendors["vendor_id"].tolist()


# ---------------------------------------------------------
# DATE RANGE
# ---------------------------------------------------------

start_date = pd.Timestamp("2024-01-01")
end_date = pd.Timestamp("2026-09-01")


# ---------------------------------------------------------
# GENERATE AP INVOICES
# ---------------------------------------------------------

ap_records = []

number_of_invoices = 3000


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
            mean=7.0,
            sigma=1.0
        ),
        2
    )

    # Approximately 75% of invoices are paid
    is_paid = random.random() > 0.25

    payment_date = None
    payment_amount = 0.0

    if is_paid:

        payment_delay = random.randint(
            -10,
            60
        )

        payment_date = due_date + pd.Timedelta(
            days=payment_delay
        )

        # Don't create payments after our dataset end date
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

    ap_records.append({

        "invoice_id":
            f"AP{i:06d}",

        "vendor_id":
            random.choice(vendor_ids),

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

df = pd.DataFrame(ap_records)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

output_file = DATA_DIR / "accounts_payable.csv"

df.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------

print("Accounts Payable data created successfully.")
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

print("Outstanding AP:")

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