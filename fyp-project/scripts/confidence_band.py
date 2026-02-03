# confidence_band.py
# Maps ONS data coverage to uncertainty multipliers for confidence bands


def confidence_multiplier(coverage_class):
    """
    Get uncertainty multiplier based on data coverage quality.
    
    Coverage -> Multiplier:
        High coverage    -> ±5%
        Partial coverage -> ±15%
        Low coverage     -> ±25%
        No coverage      -> ±40%
    
    Returns: Multiplier as decimal (e.g., 0.15 = ±15%)
    """
    
    mapping = {
        "No coverage": 0.40,
        "Low coverage": 0.25,
        "Partial coverage": 0.15,
        "High coverage": 0.05
    }
    return mapping.get(coverage_class, 0.30)


def compute_confidence_band(profit, coverage_class):
    """
    Calculate lower and upper profit bounds based on data quality.
    
    Returns: (lower_bound, upper_bound) tuple
    """
    
    m = confidence_multiplier(coverage_class)
    lower = profit * (1 - m)
    upper = profit * (1 + m)
    return lower, upper
