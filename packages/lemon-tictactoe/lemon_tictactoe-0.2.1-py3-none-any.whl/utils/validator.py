from numbers import Number

def validate_in_between(number: Number, min: Number, max: Number, value_name: str):
    if number < min or number > max:
        raise ValueError(f"{value_name} has to be a value between {min} and {max}")