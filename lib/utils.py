import math

HOUSE_COLORS = {
    "Gryffindor": "#AE0001",
    "Slytherin": "#2A623D",
    "Ravenclaw": "#222F5B",
    "Hufflepuff": "#ECB939",
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
