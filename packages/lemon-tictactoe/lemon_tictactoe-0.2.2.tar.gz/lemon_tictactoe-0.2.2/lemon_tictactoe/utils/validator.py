from typing import Any

def validate_in_between(number, min, max, value_name: str):
    if number < min or number > max:
        raise ValueError(f"{value_name} has to be a value between {min} and {max}")
    
def validate_maximum(number, max, value_name: str):
    if number > max:
        raise ValueError(f"{value_name} can only have a maximum value of {max}")
    
def validate_of_type(value: Any, required_type: type, value_name: str):
    if not isinstance(value, required_type):
        raise ValueError(f"{value_name} has to be of type {required_type.__name__}")
    
def validate_items_of_type(value_list: list, required_type: type, list_name: str, item_name: str):
    validate_of_type(value_list, list, list_name)
    for i, item in enumerate(value_list):
        if not isinstance(item, required_type):
            raise ValueError(f"{item_name} in {list_name} have to be of type {required_type.__name__}, occured at index {i}")