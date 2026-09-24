import pandas as pd
from pathlib import Path


# Project root = one level above the python folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Output folder
DATA_DIR = PROJECT_ROOT / "data"

# Make sure data folder exists
DATA_DIR.mkdir(exist_ok=True)


accounts = [
    # Revenue
    ["ACC001", "400100", "Product Revenue", "Revenue", "Income Statement"],
    ["ACC002", "400200", "Service Revenue", "Revenue", "Income Statement"],
    ["ACC003", "410100", "Other Revenue", "Revenue", "Income Statement"],

    # COGS
    ["ACC004", "500100", "Materials", "COGS", "Income Statement"],
    ["ACC005", "500200", "Direct Labor", "COGS", "Income Statement"],
    ["ACC006", "500300", "Manufacturing Overhead", "COGS", "Income Statement"],

    # Operating Expenses
    ["ACC007", "610100", "Payroll Expense", "Operating Expense", "Income Statement"],
    ["ACC008", "610200", "Office Rent", "Operating Expense", "Income Statement"],
    ["ACC009", "610300", "Technology Expense", "Operating Expense", "Income Statement"],
    ["ACC010", "610400", "Marketing Expense", "Operating Expense", "Income Statement"],
    ["ACC011", "610500", "Travel Expense", "Operating Expense", "Income Statement"],
    ["ACC012", "610600", "Professional Services", "Operating Expense", "Income Statement"],

    # Other Income / Expense
    ["ACC013", "700100", "Interest Income", "Other Income", "Income Statement"],
    ["ACC014", "710100", "Interest Expense", "Other Expense", "Income Statement"],

    # Assets
    ["ACC015", "100100", "Cash", "Asset", "Balance Sheet"],
    ["ACC016", "110100", "Accounts Receivable", "Asset", "Balance Sheet"],
    ["ACC017", "120100", "Inventory", "Asset", "Balance Sheet"],

    # Liabilities
    ["ACC018", "200100", "Accounts Payable", "Liability", "Balance Sheet"],
    ["ACC019", "210100", "Accrued Expenses", "Liability", "Balance Sheet"],

    # Equity
    ["ACC020", "300100", "Common Equity", "Equity", "Balance Sheet"],
    ["ACC021", "310100", "Retained Earnings", "Equity", "Balance Sheet"],
]


columns = [
    "account_id",
    "account_number",
    "account_name",
    "account_type",
    "financial_statement",
]


df = pd.DataFrame(accounts, columns=columns)


output_file = DATA_DIR / "chart_of_accounts.csv"

df.to_csv(output_file, index=False)


print("Chart of Accounts created successfully.")
print(f"File: {output_file}")
print(f"Rows: {len(df)}")
print()
print(df.to_string(index=False))