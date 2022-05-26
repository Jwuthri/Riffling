import re


def string_contains_digit(string: str) -> bool:
    """
    It returns True if the string contains a digit, and False otherwise

    :param string: str
    :type string: str
    :return: True or False
    """
    if re.search("\d", string):
        return True
    else:
        return False


def strike_string(string: str) -> str:
    """
    It takes a string and returns a string with each character in the original string surrounded by a combining character
    that will strike through the character

    :param string: The string to be struck through
    :type string: str
    :return: A string with the characters in the string argument struck through.
    """
    return "".join(["{}\u0336".format(c) for c in string])
