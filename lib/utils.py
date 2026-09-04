import math


HOUSE_COLORS = {
    "Gryffindor": "#e74c3c",
    "Slytherin": "#2ecc71",
    "Ravenclaw": "#3498db",
    "Hufflepuff": "#f1c40f",
}

def to_float(value: str):
    if not value:
        return None
    try:
        converted = float(value)
        if math.isnan(converted):
            return None
        return converted
    except ValueError:
        return None

