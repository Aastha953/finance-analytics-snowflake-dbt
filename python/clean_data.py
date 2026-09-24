import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


def fix_ar():
    """Fix payment amount greater than invoice amount."""

    file = DATA_DIR / "accounts_receivable.csv"

    df = pd.read_csv(file)

    invalid = df["payment_amount"] > df["invoice_amount"]

    print(
        f"AR records requiring correction: {invalid.sum()}"
    )

    # Cap payment at invoice amount
    df.loc[invalid, "payment_amount"] = (
        df.loc[invalid, "invoice_amount"]
    )

    df.to_csv(file, index=False)


def fix_sales():
    """Fix incorrect gross profit calculations."""

    file = DATA_DIR / "sales.csv"

    df = pd.read_csv(file)

    expected_profit = (
        df["revenue"] - df["cost"]
    ).round(2)

    invalid = (
        df["gross_profit"].round(2)
        != expected_profit
    )

    print(
        f"Sales records requiring correction: "
        f"{invalid.sum()}"
    )

    # Recalculate gross profit
    df.loc[invalid, "gross_profit"] = (
        df.loc[invalid, "revenue"]
        - df.loc[invalid, "cost"]
    ).round(2)

    df.to_csv(file, index=False)


def fix_gl():
    """Fix invalid GL account references."""

    file = DATA_DIR / "general_ledger.csv"

    df = pd.read_csv(file)

    coa = pd.read_csv(
        DATA_DIR / "chart_of_accounts.csv"
    )

    valid_accounts = set(
        coa["account_id"]
    )

    invalid = ~df["account_id"].isin(
        valid_accounts
    )

    print(
        f"GL records requiring correction: "
        f"{invalid.sum()}"
    )

    # Replace invalid account with a valid
    # operating expense account.
    fallback_account = (
        coa.loc[
            coa["account_type"] == "Operating Expense",
            "account_id"
        ]
        .iloc[0]
    )

    df.loc[
        invalid,
        "account_id"
    ] = fallback_account

    df.to_csv(file, index=False)


def main():

    print("\n" + "=" * 70)
    print("FINANCE DATA CLEANING")
    print("=" * 70)

    fix_ar()
    fix_sales()
    fix_gl()

    print("\n" + "=" * 70)
    print("DATA CLEANING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
    