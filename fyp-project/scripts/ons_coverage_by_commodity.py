# ons_coverage_by_commodity.py
# Calculates ONS data coverage percentage for each commodity

import pandas as pd

INPUT_FILE = "data/output/merged_hmrc_ons_commodity.csv"
OUTPUT_FILE = "data/output/ons_coverage_by_commodity_aggregated.csv"

df = pd.read_csv(INPUT_FILE, low_memory=False)

# HMRC commodity column is 'commodity_x' after merge
if "commodity_x" not in df.columns:
    raise ValueError("commodity_x column missing — merge is broken")

df = df.rename(columns={"commodity_x": "commodity"})

# Check if ONS data is present for each row
df["ons_present"] = df["import_value_million_gbp"].notna()

# Count years with ONS data per commodity
yearly = (
    df.groupby(["commodity", "year"])
      .agg(ons_present=("ons_present", "max"))
      .reset_index()
)

coverage = (
    yearly.groupby("commodity")
    .agg(
        total_years=("year", "nunique"),
        ons_covered_years=("ons_present", "sum")
    )
    .reset_index()
)

# Calculate coverage percentage
coverage["ons_coverage_pct"] = (
    coverage["ons_covered_years"] / coverage["total_years"] * 100
)

coverage = coverage.sort_values("ons_coverage_pct")
coverage.to_csv(OUTPUT_FILE, index=False)

print("Saved aggregated ONS coverage by commodity →", OUTPUT_FILE)
print(coverage.head(10))
print("Total commodities:", len(coverage))
