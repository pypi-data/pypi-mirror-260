from datetime import date

def calculate_age(birthdate):
    """Calculate age from a birthdate."""
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age
