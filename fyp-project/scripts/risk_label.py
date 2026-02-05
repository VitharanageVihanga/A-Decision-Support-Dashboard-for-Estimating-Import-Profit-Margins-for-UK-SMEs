# risk_label.py
# Classifies financial risk based on profit margin thresholds


def risk_label(margin_pct):
    """
    Classify risk level based on profit margin percentage.
    
    Thresholds:
        < 5%  -> HIGH risk (thin margins)
        5-10% -> MODERATE risk (acceptable)
        >= 10% -> LOW risk (healthy buffer)
    
    Returns: "HIGH", "MODERATE", or "LOW"
    """
    
    if margin_pct is None or margin_pct < 5:
        return "HIGH"
    elif margin_pct < 10:
        return "MODERATE"
    else:
        return "LOW"
