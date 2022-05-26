import os
import ast
import json

from typing import Dict, Any


def read_json_file(path: str) -> Dict[Any, Any]:
    """
    It reads a json file and returns a dictionary

    :param path: The path to the file to read
    :type path: str
    :return: A dictionary of any type of key and any type of value.
    """
    assert os.path.exists(path), f"file {path} doesn't exists."
    with open(path, "r") as file:
        data = json.load(file)

    return data


def read_text_file(path: str, to_object: bool = False) -> Any:
    """
    It reads a text file and returns the content as a string

    :param path: The path to the file you want to read
    :type path: str
    :param to_object: if True, the function will try to convert the text to an object, defaults to False
    :type to_object: bool (optional)
    :return: The data is being returned as a string.
    """
    assert os.path.exists(path), f"file {path} doesn't exists."
    with open(path, "r") as f:
        data = f.read()

    return data if not to_object else ast.literal_eval(data)
