def calculate_bmi(height, weight):
    """Calculate BMI using height (in meters) and weight (in kilograms)."""
    if height <= 0 or weight <= 0:
        raise ValueError("Height and weight must be greater than zero.")
    return weight / (height ** 2)
