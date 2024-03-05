from enum import Enum


def validate_enum_value(value: any, enum_class: type[Enum]) -> bool:
    if value not in enum_class.__members__.values():
        raise ValueError(f"{value} is not a valid value for {enum_class.__name__}")
    return True
