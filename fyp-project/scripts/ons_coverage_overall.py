# ons_coverage_overall.py
# Calculates overall ONS data coverage percentage by year

import pandas as pd

INPUT_FILE = "data/output/merged_hmrc_ons_totals.csv"
OUTPUT_FILE = "data/output/ons_coverage_overall_aggregated.csv"

df = pd.read_csv(INPUT_FILE, low_memory=False)

# Check ONS presence per country-year
agg = (
    df.groupby(["year", "country_code"])
    .agg(
        hmrc_rows=("value", "count"),
        ons_present=("import_value_million_gbp", lambda x: x.notna().any())
    )
    .reset_index()
)

# Calculate yearly coverage
coverage = (
    agg.groupby("year")
    .agg(
        total_country_years=("country_code", "count"),
        ons_covered_country_years=("ons_present", "sum")
    )
    .reset_index()
)

coverage["ons_coverage_pct"] = (
    coverage["ons_covered_country_years"] / coverage["total_country_years"] * 100
)

coverage.to_csv(OUTPUT_FILE, index=False)

print("Saved aggregated overall ONS coverage →", OUTPUT_FILE)
print(coverage)
