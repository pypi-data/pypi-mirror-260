from numbers import Number
from typing import Any

def validate_in_between(number: Number, min: Number, max: Number, value_name: str):
    if number < min or number > max:
        raise ValueError(f"{value_name} has to be a value between {min} and {max}")
    
def validate_of_type(value: Any, required_type: type, value_name: str):
    if not isinstance(value, required_type):
        raise ValueError(f"{value_name} has to be of type {required_type.__name__}")