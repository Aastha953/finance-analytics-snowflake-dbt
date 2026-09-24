import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")


def introduce_ar_issue():
    file = DATA_DIR / "accounts_receivable.csv"
    df = pd.read_csv(file)

    # Create an impossible payment amount
    df.loc[0, "payment_amount"] = df.loc[0, "invoice_amount"] + 5000

    df.to_csv(file, index=False)


def introduce_sales_issue():
    file = DATA_DIR / "sales.csv"
    df = pd.read_csv(file)

    # Create an incorrect gross profit calculation
    df.loc[1, "gross_profit"] = df.loc[1, "revenue"] + df.loc[1, "cost"]

    df.to_csv(file, index=False)


def introduce_gl_issue():
    file = DATA_DIR / "general_ledger.csv"
    df = pd.read_csv(file)

    # Create an invalid account reference
    df.loc[0, "account_id"] = "ACC999"

    df.to_csv(file, index=False)


def main():
    introduce_ar_issue()
    introduce_sales_issue()
    introduce_gl_issue()

    print("Data-quality issues introduced successfully.")


if __name__ == "__main__":
    main()