# classify_ons_coverage_by_commodity.py
# Classifies ONS data coverage into High/Partial/Low/No coverage

import pandas as pd

INPUT_FILE = "data/output/ons_coverage_by_commodity_aggregated.csv"
OUTPUT_FILE = "data/output/ons_coverage_by_commodity_classified.csv"

df = pd.read_csv(INPUT_FILE)

# Check required columns exist
required_cols = {"commodity", "ons_coverage_pct"}
missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")


def classify_coverage(pct):
    """
    Classify coverage percentage into categories.
    0% = No coverage, 1-40% = Low, 41-80% = Partial, 81-100% = High
    """
    if pct == 0:
        return "No coverage"
    elif pct <= 40:
        return "Low coverage"
    elif pct <= 80:
        return "Partial coverage"
    else:
        return "High coverage"


df["coverage_class"] = df["ons_coverage_pct"].apply(classify_coverage)

df.to_csv(OUTPUT_FILE, index=False)

print("Saved classified ONS coverage by commodity →", OUTPUT_FILE)
print(df[["commodity", "ons_coverage_pct", "coverage_class"]].head(10))
print("Total commodities:", len(df))
