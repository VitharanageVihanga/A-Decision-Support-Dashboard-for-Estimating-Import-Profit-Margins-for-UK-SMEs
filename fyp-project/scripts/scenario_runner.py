# scenario_runner.py
# Runs sensitivity analysis across FX and shipping cost combinations

import pandas as pd
from scripts.margin_model import compute_margin


def run_sensitivity_scenarios(
    import_value_gbp: float,
    revenue_gbp: float,
    fx_range=(-0.1, 0.1),
    shipping_range=(0.0, 0.3),
    steps=11,
    tariff_pct=0.0,
    insurance_pct=0.0,
):
    """
    Generate a grid of scenarios varying FX and shipping costs.
    
    Parameters:
        import_value_gbp: Base import value in GBP
        revenue_gbp: Expected sales revenue
        fx_range: FX shock range as decimals, default (-10%, +10%)
        shipping_range: Shipping cost range, default (0%, 30%)
        steps: Number of steps per range (11 x 11 = 121 scenarios)
        tariff_pct: Fixed tariff rate for all scenarios
        insurance_pct: Fixed insurance rate for all scenarios
    
    Returns:
        DataFrame with fx_shock_pct, shipping_pct, profit, margin_pct
    """
    
    # Generate evenly-spaced values for each range
    fx_values = [
        fx_range[0] + i * (fx_range[1] - fx_range[0]) / (steps - 1) 
        for i in range(steps)
    ]
    ship_values = [
        shipping_range[0] + i * (shipping_range[1] - shipping_range[0]) / (steps - 1) 
        for i in range(steps)
    ]
    
    # Run margin calculation for each combination
    rows = []
    for fx in fx_values:
        for ship in ship_values:
            result = compute_margin(
                import_value_gbp=import_value_gbp,
                revenue_gbp=revenue_gbp,
                fx_shock_pct=fx,
                shipping_pct=ship,
                insurance_pct=insurance_pct,
                tariff_pct=tariff_pct,
            )
            rows.append({
                "fx_shock_pct": fx * 100,
                "shipping_pct": ship * 100,
                "profit": result["profit"],
                "margin_pct": result["margin_pct"],
            })
    
    return pd.DataFrame(rows)
    
    # =========================================================================
    # STEP 3: Return as a DataFrame for easy use in the dashboard
    # =========================================================================
    # Pandas DataFrames work well with Plotly for creating heatmaps and charts.
    # The dashboard will pivot this data to create the FX × Shipping matrix.
    
    return pd.DataFrame(rows)
