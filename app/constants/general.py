from enum import Enum


class CompareOperator(Enum):
    """
    Enum for comparison operators.
    """
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    IN = "in"
    NOT_IN = "not in"
    LIKE = "like"
    NOT_LIKE = "not like"
    BETWEEN = "between"