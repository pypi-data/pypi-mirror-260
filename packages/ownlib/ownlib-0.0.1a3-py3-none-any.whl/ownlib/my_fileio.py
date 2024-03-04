from typing import Optional


def read_txt_file(filename: str) -> Optional[list]:
    try:
        with open(filename, "r") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("Невозможно открыть файл")
        data = False
    return data
