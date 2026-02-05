# margin_model.py
# Core calculation for landed cost and profit margin

def compute_margin(
    import_value_gbp: float,
    revenue_gbp: float,
    fx_shock_pct: float = 0.0,
    shipping_pct: float = 0.0,
    insurance_pct: float = 0.0,
    tariff_pct: float = 0.0,
):
    """
    Calculate landed cost and profit margin for an import scenario.
    
    Parameters:
        import_value_gbp: Base value of imported goods in GBP
        revenue_gbp: Expected sales revenue in GBP
        fx_shock_pct: Currency change as decimal (0.05 = 5% weaker GBP)
        shipping_pct: Shipping cost as % of goods value
        insurance_pct: Insurance cost as % of goods value  
        tariff_pct: Import duty as % of goods value
    
    Returns:
        Dictionary with goods_cost, shipping_cost, insurance_cost,
        tariff_cost, landed_cost, profit, margin_pct
    """
    
    # Calculate goods cost after FX adjustment
    goods_cost = import_value_gbp * (1 + fx_shock_pct)
    
    # Calculate additional costs as percentages of goods cost
    shipping_cost = goods_cost * shipping_pct
    insurance_cost = goods_cost * insurance_pct
    tariff_cost = goods_cost * tariff_pct
    
    # Total landed cost = all costs to get goods into UK
    landed_cost = goods_cost + shipping_cost + insurance_cost + tariff_cost
    
    # Safety cap: limit landed cost to 200% of import value
    MAX_COST_MULTIPLIER = 2.0
    landed_cost = min(landed_cost, import_value_gbp * MAX_COST_MULTIPLIER)
    
    # Calculate profit (capped at -100% of import value)
    profit = revenue_gbp - landed_cost
    profit = max(profit, -import_value_gbp)
    
    # Calculate margin percentage
    if revenue_gbp > 0:
        margin_pct = (profit / revenue_gbp) * 100
        margin_pct = max(margin_pct, -100)
    else:
        margin_pct = None
    
    return {
        "goods_cost": round(goods_cost, 2),
        "shipping_cost": round(shipping_cost, 2),
        "insurance_cost": round(insurance_cost, 2),
        "tariff_cost": round(tariff_cost, 2),
        "landed_cost": round(landed_cost, 2),
        "profit": round(profit, 2),
        "margin_pct": round(margin_pct, 2) if margin_pct is not None else None,
    }
