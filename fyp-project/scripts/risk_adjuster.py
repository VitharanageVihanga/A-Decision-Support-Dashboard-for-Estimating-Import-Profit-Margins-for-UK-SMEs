# risk_adjuster.py
# Adjusts risk level based on ONS data coverage quality


def adjust_risk(margin_risk: str, coverage_class: str) -> str:
    """
    Adjust risk level based on data quality.
    
    Rules:
        - HIGH risk stays HIGH
        - MODERATE becomes HIGH if poor data coverage
        - LOW becomes MODERATE if poor data coverage
    
    Parameters:
        margin_risk: Base risk from risk_label() - "HIGH", "MODERATE", or "LOW"
        coverage_class: ONS coverage - "High/Partial/Low/No coverage"
    
    Returns: Adjusted risk level
    """
    
    # HIGH risk can't get worse
    if margin_risk == "HIGH":
        return "HIGH"
    
    # MODERATE risk -> HIGH if poor data
    if margin_risk == "MODERATE":
        if coverage_class in ["No coverage", "Low coverage"]:
            return "HIGH"
        return "MODERATE"
    
    # LOW risk -> MODERATE if poor data
    if margin_risk == "LOW":
        if coverage_class in ["No coverage", "Low coverage"]:
            return "MODERATE"
        return "LOW"
    
    return margin_risk
