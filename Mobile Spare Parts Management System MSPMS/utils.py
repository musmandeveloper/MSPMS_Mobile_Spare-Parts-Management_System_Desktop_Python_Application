

# Utilities (Helper Functions)


# NOTE: The utils.py file can include various helper functions that are used across multiple modules 
# in your application.


# utils.py


def validate_input(*args):
    """
    Validates if all the provided inputs are non-empty.
    :param args: List of inputs to validate.
    :return: Boolean indicating if all inputs are valid.
    """
    for arg in args:
        if not arg or arg.strip() == "":
            return False
    return True

def format_currency(value):
    """
    Formats a decimal value as currency.
    :param value: Decimal value to format.
    :return: Formatted string representing the currency.
    """
    return "${:,.2f}".format(value)



