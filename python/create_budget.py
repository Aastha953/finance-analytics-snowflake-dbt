"""
Budget generator v2: driven by actual GL activity.

v1 used np.random.uniform(10000, 100000) per month x account x cost center,
producing a ~$243.6M budget vs ~$34.4M actual (14% attainment).
v2 sets budget = actual GL net amount x planning variance (85%-125%).
Combinations with no GL activity get $0 budget (no random fallback).
The existing month x account x cost center grid (4,455 rows) is preserved.
"""
import numpy as np
import pandas as pd
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"
rng = np.random.default_rng(42)  # reproducible

budget = pd.read_csv(DATA / "budget.csv")
gl = pd.read_csv(DATA / "general_ledger.csv")

budget["_month"] = pd.to_datetime(budget["budget_month"]).dt.to_period("M")
gl["_month"] = pd.to_datetime(gl["transaction_date"]).dt.to_period("M")
gl["net_amount"] = gl["debit"].fillna(0) - gl["credit"].fillna(0)

actuals = (
    gl.groupby(["_month", "account_id", "cost_center_id"], as_index=False)["net_amount"]
      .sum()
      .rename(columns={"net_amount": "actual_amount"})
)

out = budget.drop(columns=["budget_amount"]).merge(
    actuals, on=["_month", "account_id", "cost_center_id"], how="left"
)
out["actual_amount"] = out["actual_amount"].fillna(0)

# Planning variance: budgets typically land slightly above actual spend
variance = rng.normal(loc=1.03, scale=0.08, size=len(out)).clip(0.85, 1.25)
out["budget_amount"] = (out["actual_amount"].abs() * variance).round(2)

zero_cells = (out["actual_amount"] == 0).sum()
total_actual = out["actual_amount"].abs().sum()
total_budget = out["budget_amount"].sum()

out[["budget_month", "account_id", "cost_center_id", "budget_amount"]].to_csv(
    DATA / "budget.csv", index=False
)

print(f"Rows written:          {len(out):,}")
print(f"Cells with no activity: {zero_cells:,} (budget = 0)")
print(f"Total actual (grid):   ${total_actual:,.2f}")
print(f"Total budget:          ${total_budget:,.2f}")
print(f"Attainment:            {total_actual / total_budget:.2%}")