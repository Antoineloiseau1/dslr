import math

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
