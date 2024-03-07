"""Small useful file manipulating functions"""
from typing import Union


def read_txt_file(filename: str) -> Union[list, None]:
    """
    TODO Add some description
    """
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("Невозможно открыть файл")
        data = None
    return data
