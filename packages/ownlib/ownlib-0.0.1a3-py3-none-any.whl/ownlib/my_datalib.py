import pandas as pd
from loguru import logger
from typing import Any, Union, Tuple

from ownlib.mytinylib import is_empty


def save2csv(data2save: pd.DataFrame, path2save: str) -> bool:
    """Save results in csv file

    :param data2save: pd.DataFrame
    :param path2save: str, Storage file path
    :returns: result_flag: bool, True / False
    """
    try:
        print(type(data2save))
        data2save.to_csv(path2save)
        print(f"File save successful.")
        result_flag: bool = True
    except Exception as ex:
        print(f"File saving error, {ex}.")
        result_flag: bool = False
    return result_flag


def save2xlsx(data2save: pd.DataFrame, path2save: str) -> bool:
    """
    Save results in xlsx file

    :param data2save: DataFrame
    :param path2save: Storage file path
    :returns: result_flag: bool, True / False
    """
    result_flag: bool = False
    try:
        with pd.ExcelWriter(path2save) as writer:
            data2save.to_excel(writer, sheet_name='отчёт')
        print(f"Data save to <{path2save}>")
        result_flag = True
    except Exception as file_saving_error:
        logger.error(f"File save error, {file_saving_error}.")
        result_flag = False

    return result_flag


def dict_print(arg: dict):
    dict2print = ''
    for note in arg.values():
        # TODO Thought about `if bool(note):` in below line
        if not is_empty(note):
            dict2print += '/' + str(note)
    return dict2print


# TODO - Check refactoring function name in my projects
def iterable_data(arg: Any) -> bool:
    """
    Shadow of is_iterable()

    :param arg:
    :return:
    """
    return is_iterable(arg)


def is_iterable(arg: Any) -> bool:
    """
    Iterable and non string data checking
    ___
    :param arg: any data
    :returns: True / False
    """
    import six

    return (
            isinstance(arg, six.Iterator)
            and not isinstance(arg, six.string_types)
    )


def expand2list(data) -> list:
    """
    Flatten data structure to list

    :param data: iterable (non string) data structure
    :returns: list
    """
    #     logger.disable(__name__)
    func_result: list = []
    if isinstance(data, dict):
        logger.warning(f"[!] The <element> is of type <dict>, only the <element.values()> is processing.")
        data = data.values()

    for element in data:
        if iterable_data(element):
            flatting_element = expand2list(element)
            [func_result.append(field) for field in flatting_element]
        else:
            func_result.append(element)

    logger.debug(f"{func_result=}")
    #     logger.enable(__name__)
    return func_result


def true_mask(data: pd.DataFrame) -> pd.Series:
    """
    Get whole <True> pd.DataFrame mask of original dataframe

    :param data: pd.DataFrame - original dataframe
    :return: pd.Series - <True> mask of data
    """
    return data[data.columns[0]].notna()


def supplemented_list(master: list, proposing_list: Union[list, tuple], request_kind: str = 'supplement') -> list:
    """
    Supplementing the main list with new unique entries\n
    ----
    :param master: list - previously stored list
    :param proposing_list: list - list of candidates to be added to the master
    :param request_kind: str - kind of returned data (default - supplemented list), 'new' - only new items list
    :return: result list
    """
    assert len(set(proposing_list)) == len(proposing_list), '[!] Non-unique proposing items finding.'
    assert request_kind in ('new', 'supplement'), f'[!] Wrong request_kind value: <{request_kind}>.'

    non_in_master_items = [item for item in proposing_list if item not in master]

    if request_kind == 'supplement':
        master.extend(non_in_master_items)
        response = master
    else:
        response = non_in_master_items

    return response


def get_chain_attribs(item: object, attribs: str = '', default=None):
    """
    get_chain_attribs(item, attribs[, default]) -> value\n

    Get a named attribute from an object; get_chain_attribs(x, 'a.b.c') is equivalent to x.a.b.c\n
    When attribs is empty, return whole object\n
    Default argument == None or given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.\n
    ----\n
    :param item: object: - analysing object
    :param attribs: str: - attribute chain
    :param default: default return in case absent of attribs in item
    :return: value of item.attribs
    """
    logger.disable(__name__)
    # logger.enable(__name__)
    # logger.info(f"{__name__=}")
    get_chain_attribs.attr = item
    if attribs:
        for note in attribs.split('.'):
            try:
                logger.debug(f"Get <{note}> in {attribs=}")
                get_chain_attribs.attr = getattr(get_chain_attribs.attr, note, default)
                logger.debug(f"Got {get_chain_attribs.attr=}")
            except AttributeError:
                logger.warning(f"[!] Absent attribute: <{note}> in\n<{item}>")
                return default
            except Exception as unknown_exception:
                logger.warning(f"[!] Unknown error in requested attribute: <{note}>")
                raise unknown_exception
    else:
        logger.warning(f"[?] No attribute in requested {attribs=}")

    return get_chain_attribs.attr


def get_object_by_pattern(pattern: str,
                          objects: Union[list, tuple, set], attribs: str = 'name',
                          exact: bool = True) -> Union[object, None]:
    """
    Search object in iterator ("objects" here) by value of attribute <name>\n
    ----\n
    :param pattern: str: - goal value
    :param objects: - objects iterator
    :param attribs: str: - attribs chain (object, 'a.b.c') -> object.a.b.c
    :param exact: bool: - Exact match filtering, if False - non-exact match, multiply items return possible!
    :return: object: - Success search result object in case single filter result,
                       tuple in case multiply result, or None empty result.
    """

    logger.disable(__name__)
    # logger.enable(__name__)
    # logger.debug(f"[*] Check <{pattern=}>, contains in {attribs=} for {objects=}")

    def stringFilter(checking_string):
        if exact:
            return pattern.lower() == checking_string.lower()
        return pattern.lower() in checking_string.lower()

    def objectFilter(checking_object) -> bool:
        logger.debug(f"{checking_object=}")
        object_attribute_value = get_chain_attribs(checking_object, attribs)
        logger.debug(f"{object_attribute_value=}")
        if exact:
            return pattern.lower() == object_attribute_value.lower()
        return pattern.lower() in object_attribute_value.lower()

    try:
        search_result = tuple(filter(objectFilter, objects))
        logger.debug(f"*** OBJECT FOUND:\n{search_result=}")
    except TypeError:
        logger.error(f"[!] Wrong attribute type: {attribs=}")
        return None

    # logger.debug(f"{len(search_result)=}")
    if len(search_result) > 1:
        logger.info(f"[!] Non single filter result")
    elif len(search_result) == 1:
        search_result = search_result[0]
    elif not search_result:
        logger.warning(f"[!] Object with <{pattern=}>, {attribs=} not found in {objects=}")
        search_result = None
    logger.debug(f"Return: {search_result}")

    return search_result


def distribute_by_order(iterator: Union[tuple, list], order: Union[tuple, list]) -> Union[list, None]:
    """
    Return ordered iterator items or None in case incorrect indexes sequence (order).\n
    ----\n
    :param iterator: - items warehouse
    :param order: - sequence of iterator indexes as set of return order rules. Indexes
    :return: Items of iterator according to the order list.
    """
    assert len(iterator) == len(order), f"[!] Iterator length not equal indices quantity!"
    try:
        sequence = (iterator[idx] for idx in order)
    except IndexError:
        logger.error(f"Wrong index in <{order=}>, return None")
        sequence = None
    except Exception as ex:
        raise Exception(ex)
    return sequence
    
    
QUANTITY_SUFFIXES = ('штук', 'штука', 'штуки', 'штук')
MONEY_SUFFIXES = ('рублей', 'рубль', 'рубля', 'рублей')


def numeral_suffix(value: Union[int, float],
                   suffix_variants: Tuple[str, str, str, str] = ('лет',
                                                                 'год',
                                                                 'года',
                                                                 'лет')) -> str:
    """Add value dependent numeral suffix.  (!) russian only

    :param value: int - age
    :param suffix_variants: tuple - suffix variants
    :return: _numeral_suffix: str - numeral depends string
    """
    _numeral_suffix = ''
    if 11 <= value % 100 <= 19:
        _numeral_suffix = suffix_variants[0]
    elif value % 10 == 1:
        _numeral_suffix = suffix_variants[1]
    elif 2 <= value % 10 <= 4:
        _numeral_suffix = suffix_variants[2]
    else:
        _numeral_suffix = suffix_variants[3]

    return _numeral_suffix

