"""Generate reproducible summary outputs for the APL Logistics project."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "APL_Logistics.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

try:
    df = pd.read_csv(DATA, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(DATA, encoding="latin1")

df.columns = df.columns.str.strip()
for col in ["Sales", "Order Profit Per Order", "Order Item Discount",
            "Order Item Discount Rate", "Order Item Profit Ratio"]:
    if col in df:
        df[col] = pd.to_numeric(df[col], errors="coerce")

valid = df["Sales"].notna() & df["Order Profit Per Order"].notna() & (df["Sales"] > 0)
clean = df.loc[valid].copy()
clean["Profit Margin (%)"] = clean["Order Profit Per Order"] / clean["Sales"] * 100

summary = pd.DataFrame([
    {"Metric": "Original rows", "Value": len(df)},
    {"Metric": "Rows used", "Value": len(clean)},
    {"Metric": "Unique customers", "Value": clean["Order Customer Id"].nunique()},
    {"Metric": "Unique products", "Value": clean["Product Name"].nunique()},
    {"Metric": "Unique categories", "Value": clean["Category Name"].nunique()},
    {"Metric": "Total revenue", "Value": clean["Sales"].sum()},
    {"Metric": "Total profit", "Value": clean["Order Profit Per Order"].sum()},
    {"Metric": "Overall profit margin (%)", "Value": clean["Order Profit Per Order"].sum() / clean["Sales"].sum() * 100},
    {"Metric": "Negative-profit rows", "Value": int((clean["Order Profit Per Order"] < 0).sum())},
    {"Metric": "Exact duplicate rows in original", "Value": int(df.duplicated().sum())},
])
summary.to_csv(OUT / "overall_summary.csv", index=False)

for label, group_col in [
    ("customer_profitability", "Order Customer Id"),
    ("product_profitability", "Product Name"),
    ("category_profitability", "Category Name"),
    ("market_profitability", "Market"),
    ("region_profitability", "Order Region"),
    ("country_profitability", "Order Country"),
]:
    if group_col not in clean:
        continue
    grouped = clean.groupby(group_col, dropna=False).agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Rows=("Sales", "size")
    ).reset_index()
    grouped["Profit Margin (%)"] = grouped["Profit"] / grouped["Revenue"].replace(0, pd.NA) * 100
    grouped.sort_values("Profit", ascending=False).to_csv(OUT / f"{label}.csv", index=False)

print(f"Analysis complete. Summary files saved to: {OUT}")
print(summary.to_string(index=False))
