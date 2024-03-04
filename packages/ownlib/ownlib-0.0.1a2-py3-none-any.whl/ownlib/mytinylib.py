"""
Short useful functions library
"""
from typing import (Any,
                    Tuple,
                    Union
)
import os
from glob import glob
import pathlib
from hashlib import md5

from datetime import datetime
import pandas
from IPython.display import clear_output

from loguru import logger

from ownlib.txt_lib import (digit_only,
                            EMPTY_STR
)


def non_filtering_mask(data_frame: pandas.DataFrame) -> pandas.DataFrame:
    """
    Prepare a non-filtering mask with a shape and columns similar to the tmp_df
    :param data_frame: Pandas.DataFrame, for which prep the mask
    :return: Non-filtering mask
    """
    return data_frame.mask(data_frame.notnull(), True)


def is_empty(arg) -> bool:
    """Check arg not ( 0 | None | len(arg) == 0 )"""
    flag = False
    if arg is not None:
        if isinstance(arg, (int, float, complex)) and arg == 0:
            flag = True
        else:
            try:
                if not arg:
                    flag = True
            except Exception as ex:
                logger.error(f"Unsupported data type {arg=}, {type(arg)=}, {ex=}")
                flag = False
    else:
        flag = True
    return flag


def read_txt_file(filename: str):
    """
    TODO add some description
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = file.readlines()
    except FileNotFoundError:
        print("Невозможно открыть файл")
        data = False
    return data


def repeated_string(repeat_num: int,
                    string_pattern: str = '*',
                    postfix: str = EMPTY_STR,
                    drop_last_insert: bool = True) -> str:
    """
    Make repeated patterns string

    :param repeat_num: int, num of repeating
    :param string_pattern: str, repeated pattern (default = '*')
    :param postfix: str, pattern, inserting between two char_pattern
    :param drop_last_insert: bool, drop last insert_pattern if True (default)
    :returns: str, like (char_pattern + insert_pattern) * repeat_num
    """
    hyper_pattern = string_pattern + postfix
    got_string = hyper_pattern * repeat_num
    if drop_last_insert:
        got_string = got_string[:len(got_string) - len(postfix)]

    return got_string


def show_choices(choices: list, axe: str = 'v'):
    """
        TODO add some description
    """
    if axe == 'v':
        max_chars_in_item = max(choices, key=len, default=0)
        max_chars_in_idx = len(str(len(choices)))
        max_line_length = max_chars_in_idx + 2 + max_chars_in_item
        div_line = repeated_string(max_line_length)

        print(div_line)
        for i, item in enumerate(choices):
            print(f"{i}: {item}")
        print(div_line)
    # TODO THOUGHT ABOUT THIS CASE NECESSARY
    elif axe == 'h':
        choices_in_line = '  '.join(f"{i}:{variant}" for i, variant in enumerate(choices))
        div_line = repeated_string(len(choices_in_line))
        print(div_line)
        print(choices_in_line)
        print(div_line)
    else:
        logger.error(f"[!] Unknown {axe=}")


def show_warning(message: Any):
    """
    Show warning message
    :param message:
    :return: None
    """
    print(f"[!] Wrong input value: {message}")


def last_index(iterator: list) -> int:
    """
    Return last iterator index\n
    :param iterator: - list for example
    :return: last index in iterator
    """
    return len(iterator) - 1


def get_choice_position(choices: list, axe: str = 'v') -> Union[int, None]:
    """
    Type choices list and request choice position from user.\n
    In case incorrect choice position - clear output and start again.\n
    :param choices: list: list of choices (filenames for example)
    :param axe: str: 'v'(default) - vertical or 'h' - horizontal data print mode
    :return: int: choice position in the list or Null if empty / wrong user input
    """
    logger.disable(__name__)
    choices = choices.copy()
    choices.append('Exit')
    index_range = range(len(choices))
    choice_position = max_index = last_index(choices)

    while choice_position in index_range:
        print("Select choices:")
        show_choices(choices, axe)
        choice_position = input(f"\nEnter choice position < from 0 to {max_index} >, "
                                f"empty input for quit:")
        logger.debug(f"{choice_position=}")
        if choice_position == '' or choice_position == str(max_index):
            choice_position = None
            break
        try:
            choice_position = int(choice_position)
        except ValueError:
            # clear_output()
            # os.system('clr||clear')
            show_warning(choice_position)
            choice_position = max_index
            continue
        if choice_position in index_range[:-1]:
            logger.success(f"Chosen {choice_position=}")
            break
        else:
            # clear_output()
            # os.system('clr||clear')
            show_warning(choice_position)
            choice_position = last_index(choices)

    return choice_position


def get_file_name(filename_pattern: str = '*.*',
                  mask_by: str = None,
                  reverse: bool = False) -> tuple:
    """
    TODO Fill function description text!
    TODO absent reverse mode
    :param filename_pattern: str, pattern for filtering file name
    :param mask_by: str, filtering mode (recently - recent (newest file)
    :param reverse: bool, sorting mode, default is False
    :returns: tuple, file info, file name, found by conditions
    """
    logger.disable(__name__)
    filenames = glob(filename_pattern)
    logger.debug(f"Next files founded by filtering with <{filename_pattern}>:")
    logger.debug('\n' + '\n'.join(filenames))
    ordered_filename = EMPTY_STR
    files_info = []
    for filename in filenames:
        f_name = pathlib.Path(filename)
        create_date = datetime.fromtimestamp(f_name.stat().st_mtime)
        files_info.append({"name": filename, "date": create_date})

    names = [note['name'] for note in files_info]
    dates = [note['date'] for note in files_info]
    if mask_by == 'recently':
        recently = max(dates)
        recent_filename = [name for name, date in zip(names, dates) if date == recently]
        ordered_filename = recent_filename

    return files_info, ordered_filename


def edit_df_row(original_df: pandas.DataFrame,
                row_arg = EMPTY_STR) -> Tuple[pandas.DataFrame, int]:
    """
    Maybe need atomizing (too large)?
    TODO Fill function description text
    TODO: Though about using get_choice_position() here
    :param original_df: pandas.DataFrame - source Pandas DataFrame
    :param row_arg: str - user`s input
    :return: Tuple[pandas.DataFrame, int] - result (DataFrame, edited row index)
    """
    edited_df = original_df.copy()
    row_arg = str(row_arg)
    editing_row_index = None
    while row_arg.lower() != 'exit':
        if row_arg == EMPTY_STR or not digit_only(row_arg):
            row_arg = input('\n' + '[?] Enter index row to edit (integer):')
        try:
            editing_row_index = int(row_arg)
        except ValueError:
            print('[!] Integer only, please!')
            continue
        row2edit = edited_df.iloc[editing_row_index,]
        print("[>] Edit row:", "\n", row2edit, "\n")
        print("[!] Field for editing", "\n\t", "SELECT", "\t", "FIELD NAME")

        menu_items = edited_df.columns.to_list()
        menu_items.append('Exit')
        logger.debug(f"{menu_items=}")
        for menu_idx, menu_point in enumerate(menu_items):
            print("\t" + f"{round(menu_idx, 2)}" + "\t" + f"{menu_point}")
        column_num2edit = int(input('[?] Enter SELECT FIELD NAME, to edit:'))
        if column_num2edit == len(menu_items) - 1:
            break
        label2edit = menu_items[column_num2edit]
        print(f"[>] Edit {label2edit}")
        field4edit = edited_df.iloc[editing_row_index, column_num2edit]
        field_type = type(field4edit)
        print(f"[>] Original value: <{field4edit}>, {type(field4edit)}")
        new_value = input("[?] New value:")
        new_value = field_type(new_value)
        print(f"[>] Set new state: {new_value}, {type(new_value)}")
        edited_df.iloc[editing_row_index, column_num2edit] = new_value
        print("[>] Edited row:", '\n', edited_df.iloc[editing_row_index,])
        clear_output()
        os.system('clr||clear')

    print("Editing closed")

    return edited_df, editing_row_index


def get_md5(*args) -> str:
    """
    TODO add some description
    """
    try:
        data_for_md5: bytes = EMPTY_STR.join(args).encode('utf8')
    except TypeError:
        logger.exception('Type error', args)
        raise
    function_result = md5(data_for_md5).hexdigest()
    logger.debug(f"{args=}" + 'n' + f"{function_result}")

    return function_result


def chosen_filename(file_mask: str = '*.*') -> Union[str, None]:
    """
    Request user and return name of chosen file or None in case empty or last point user input

    :param file_mask:
    :return: str: filename [!] ONLY. \
    Without previously parts of path ([any/.../]filename) or None when Exit
    """
    ls_list = get_file_name(file_mask)[0]
    files_list = [note['name'] for note in ls_list]
    files_list.sort()
    user_choice = get_choice_position(files_list)
    if user_choice is not None:
        chosen_name = files_list[user_choice]
        if '/' in chosen_name:
            chosen_name = chosen_name.split('/')[-1]
    else:
        chosen_name = user_choice

    return chosen_name
