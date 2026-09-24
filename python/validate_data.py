import pandas as pd
from pathlib import Path


# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path("data")

FILES = [
    "chart_of_accounts.csv",
    "cost_centers.csv",
    "entities.csv",
    "customers.csv",
    "vendors.csv",
    "sales.csv",
    "accounts_receivable.csv",
    "accounts_payable.csv",
    "general_ledger.csv",
    "budget.csv",
    "forecast.csv",
]


# ============================================================
# 1. BASIC FILE VALIDATION
# ============================================================

def validate_file(file_name):
    """Validate basic structure, nulls, duplicates and data types."""

    path = DATA_DIR / file_name
    df = pd.read_csv(path)

    print("\n" + "=" * 70)
    print(f"FILE: {file_name}")
    print("=" * 70)

    # Row and column counts
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")

    # --------------------------------------------------------
    # Null validation
    # --------------------------------------------------------

    nulls = df.isnull().sum()
    nulls = nulls[nulls > 0]

    if len(nulls) > 0:
        print("\nNULL VALUES:")
        print(nulls)
    else:
        print("\nNULL VALUES: None")

    # --------------------------------------------------------
    # Duplicate validation
    # --------------------------------------------------------

    duplicates = df.duplicated().sum()

    print(
        f"\nDuplicate rows: {duplicates:,}"
    )

    # --------------------------------------------------------
    # Data types
    # --------------------------------------------------------

    print("\nData types:")
    print(df.dtypes)


# ============================================================
# 2. ACCOUNTS RECEIVABLE VALIDATION
# ============================================================

def validate_ar():
    """Validate Accounts Receivable business rules."""

    df = pd.read_csv(
        DATA_DIR / "accounts_receivable.csv"
    )

    print("\n" + "=" * 70)
    print("AR BUSINESS RULE VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Payment cannot exceed invoice amount
    # --------------------------------------------------------

    invalid_payment = df[
        df["payment_amount"] > df["invoice_amount"]
    ]

    print(
        f"Payments greater than invoice amount: "
        f"{len(invalid_payment):,}"
    )

    # --------------------------------------------------------
    # Due date cannot be before invoice date
    # --------------------------------------------------------

    invoice_date = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )

    due_date = pd.to_datetime(
        df["due_date"],
        errors="coerce"
    )

    invalid_dates = df[
        due_date < invoice_date
    ]

    print(
        f"Due date before invoice date: "
        f"{len(invalid_dates):,}"
    )

    # --------------------------------------------------------
    # Negative invoice amounts
    # --------------------------------------------------------

    negative_invoice = df[
        df["invoice_amount"] < 0
    ]

    print(
        f"Negative invoice amounts: "
        f"{len(negative_invoice):,}"
    )

    # --------------------------------------------------------
    # Negative payment amounts
    # --------------------------------------------------------

    negative_payment = df[
        df["payment_amount"] < 0
    ]

    print(
        f"Negative payment amounts: "
        f"{len(negative_payment):,}"
    )


# ============================================================
# 3. ACCOUNTS PAYABLE VALIDATION
# ============================================================

def validate_ap():
    """Validate Accounts Payable business rules."""

    df = pd.read_csv(
        DATA_DIR / "accounts_payable.csv"
    )

    print("\n" + "=" * 70)
    print("AP BUSINESS RULE VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Payment cannot exceed invoice amount
    # --------------------------------------------------------

    invalid_payment = df[
        df["payment_amount"] > df["invoice_amount"]
    ]

    print(
        f"Payments greater than invoice amount: "
        f"{len(invalid_payment):,}"
    )

    # --------------------------------------------------------
    # Due date cannot be before invoice date
    # --------------------------------------------------------

    invoice_date = pd.to_datetime(
        df["invoice_date"],
        errors="coerce"
    )

    due_date = pd.to_datetime(
        df["due_date"],
        errors="coerce"
    )

    invalid_dates = df[
        due_date < invoice_date
    ]

    print(
        f"Due date before invoice date: "
        f"{len(invalid_dates):,}"
    )

    # --------------------------------------------------------
    # Negative invoice amounts
    # --------------------------------------------------------

    negative_invoice = df[
        df["invoice_amount"] < 0
    ]

    print(
        f"Negative invoice amounts: "
        f"{len(negative_invoice):,}"
    )

    # --------------------------------------------------------
    # Negative payment amounts
    # --------------------------------------------------------

    negative_payment = df[
        df["payment_amount"] < 0
    ]

    print(
        f"Negative payment amounts: "
        f"{len(negative_payment):,}"
    )


# ============================================================
# 4. SALES VALIDATION
# ============================================================

def validate_sales():
    """Validate Sales business rules."""

    df = pd.read_csv(
        DATA_DIR / "sales.csv"
    )

    print("\n" + "=" * 70)
    print("SALES BUSINESS RULE VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Gross profit must equal revenue - cost
    # --------------------------------------------------------

    expected_profit = (
        df["revenue"] - df["cost"]
    ).round(2)

    actual_profit = (
        df["gross_profit"]
    ).round(2)

    invalid_profit = df[
        actual_profit != expected_profit
    ]

    print(
        f"Gross profit calculation errors: "
        f"{len(invalid_profit):,}"
    )

    # --------------------------------------------------------
    # Negative revenue
    # --------------------------------------------------------

    negative_revenue = df[
        df["revenue"] < 0
    ]

    print(
        f"Negative revenue: "
        f"{len(negative_revenue):,}"
    )

    # --------------------------------------------------------
    # Negative cost
    # --------------------------------------------------------

    negative_cost = df[
        df["cost"] < 0
    ]

    print(
        f"Negative cost: "
        f"{len(negative_cost):,}"
    )


# ============================================================
# 5. FORECAST VALIDATION
# ============================================================

def validate_forecast():
    """Validate Forecast business rules."""

    df = pd.read_csv(
        DATA_DIR / "forecast.csv"
    )

    print("\n" + "=" * 70)
    print("FORECAST VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Negative forecast amounts
    # --------------------------------------------------------

    negative_forecast = df[
        df["forecast_amount"] < 0
    ]

    print(
        f"Negative forecast amounts: "
        f"{len(negative_forecast):,}"
    )

    # --------------------------------------------------------
    # Forecast versions
    # --------------------------------------------------------

    print("\nForecast versions:")

    print(
        df["forecast_version"].value_counts()
    )


# ============================================================
# 6. FOREIGN KEY VALIDATION
# ============================================================

def validate_foreign_keys():
    """Validate relationships between source tables."""

    print("\n" + "=" * 70)
    print("FOREIGN KEY VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Reference / dimension tables
    # --------------------------------------------------------

    coa = pd.read_csv(
        DATA_DIR / "chart_of_accounts.csv"
    )

    cost_centers = pd.read_csv(
        DATA_DIR / "cost_centers.csv"
    )

    entities = pd.read_csv(
        DATA_DIR / "entities.csv"
    )

    customers = pd.read_csv(
        DATA_DIR / "customers.csv"
    )

    vendors = pd.read_csv(
        DATA_DIR / "vendors.csv"
    )

    # --------------------------------------------------------
    # Transaction / fact tables
    # --------------------------------------------------------

    sales = pd.read_csv(
        DATA_DIR / "sales.csv"
    )

    ar = pd.read_csv(
        DATA_DIR / "accounts_receivable.csv"
    )

    ap = pd.read_csv(
        DATA_DIR / "accounts_payable.csv"
    )

    gl = pd.read_csv(
        DATA_DIR / "general_ledger.csv"
    )

    budget = pd.read_csv(
        DATA_DIR / "budget.csv"
    )

    forecast = pd.read_csv(
        DATA_DIR / "forecast.csv"
    )

    # --------------------------------------------------------
    # Relationships to validate
    # --------------------------------------------------------

    checks = {
        "Sales → Customers": (
            sales["customer_id"],
            customers["customer_id"]
        ),

        "AR → Customers": (
            ar["customer_id"],
            customers["customer_id"]
        ),

        "AP → Vendors": (
            ap["vendor_id"],
            vendors["vendor_id"]
        ),

        "GL → Chart of Accounts": (
            gl["account_id"],
            coa["account_id"]
        ),

        "GL → Cost Centers": (
            gl["cost_center_id"],
            cost_centers["cost_center_id"]
        ),

        "GL → Entities": (
            gl["entity_id"],
            entities["entity_id"]
        ),

        "Budget → Chart of Accounts": (
            budget["account_id"],
            coa["account_id"]
        ),

        "Forecast → Chart of Accounts": (
            forecast["account_id"],
            coa["account_id"]
        ),
    }

    # --------------------------------------------------------
    # Execute FK checks
    # --------------------------------------------------------

    for name, (child, parent) in checks.items():

        invalid = ~child.isin(parent)

        print(
            f"{name}: "
            f"{invalid.sum():,} invalid references"
        )


# ============================================================
# 7. GENERAL LEDGER INTEGRITY VALIDATION
# ============================================================

def validate_gl_integrity():
    """Validate General Ledger accounting integrity."""

    gl = pd.read_csv(
        DATA_DIR / "general_ledger.csv"
    )

    print("\n" + "=" * 70)
    print("GENERAL LEDGER INTEGRITY VALIDATION")
    print("=" * 70)

    # --------------------------------------------------------
    # Check 1:
    # Transaction should not have both debit and credit.
    # --------------------------------------------------------

    both_debit_credit = gl[
        (gl["debit"] > 0) &
        (gl["credit"] > 0)
    ]

    print(
        f"Transactions with both debit and credit: "
        f"{len(both_debit_credit):,}"
    )

    # --------------------------------------------------------
    # Check 2:
    # Transaction should have either debit or credit.
    # --------------------------------------------------------

    zero_transactions = gl[
        (gl["debit"] == 0) &
        (gl["credit"] == 0)
    ]

    print(
        f"Transactions with zero debit and credit: "
        f"{len(zero_transactions):,}"
    )

    # --------------------------------------------------------
    # Check 3:
    # Debit should not be negative.
    # --------------------------------------------------------

    negative_debit = gl[
        gl["debit"] < 0
    ]

    print(
        f"Negative debit amounts: "
        f"{len(negative_debit):,}"
    )

    # --------------------------------------------------------
    # Check 4:
    # Credit should not be negative.
    # --------------------------------------------------------

    negative_credit = gl[
        gl["credit"] < 0
    ]

    print(
        f"Negative credit amounts: "
        f"{len(negative_credit):,}"
    )

    # --------------------------------------------------------
    # Check 5:
    # Overall debit / credit totals.
    #
    # The current synthetic GL is simplified and does not
    # contain complete journal-entry pairs.
    # Therefore this is informational.
    # --------------------------------------------------------

    total_debit = gl["debit"].sum()
    total_credit = gl["credit"].sum()

    difference = (
        total_debit - total_credit
    )

    print(
        f"\nTotal Debit:  "
        f"${total_debit:,.2f}"
    )

    print(
        f"Total Credit: "
        f"${total_credit:,.2f}"
    )

    print(
        f"Debit/Credit Difference: "
        f"${difference:,.2f}"
    )


# ============================================================
# 8. MAIN VALIDATION PROCESS
# ============================================================

def main():

    print("\n")
    print("=" * 70)
    print("FINANCE ANALYTICS DATA QUALITY REPORT")
    print("=" * 70)

    # --------------------------------------------------------
    # Basic validation for all source files
    # --------------------------------------------------------

    for file_name in FILES:
        validate_file(file_name)

    # --------------------------------------------------------
    # Business-rule validation
    # --------------------------------------------------------

    validate_ar()

    validate_ap()

    validate_sales()

    validate_forecast()

    # --------------------------------------------------------
    # Referential-integrity validation
    # --------------------------------------------------------

    validate_foreign_keys()

    # --------------------------------------------------------
    # General Ledger validation
    # --------------------------------------------------------

    validate_gl_integrity()

    # --------------------------------------------------------
    # Complete
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)


# ============================================================
# RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    main()