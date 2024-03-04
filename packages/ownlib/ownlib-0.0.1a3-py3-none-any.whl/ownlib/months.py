from pandas import DataFrame
from numpy import array

from loguru import logger

months_df = DataFrame(array([['Январь', 'January'],
                             ['Февраль', 'February'],
                             ['Март', 'March'],
                             ['Апрель', 'April'],
                             ['Май', 'May'],
                             ['Июнь', 'June'],
                             ['Июль', 'July'],
                             ['Август', 'August'],
                             ['Сентябрь', 'September'],
                             ['Октябрь', 'October'],
                             ['Ноябрь', 'November'],
                             ['Декабрь', 'December']]),
                      columns=['russian', 'english']
                      )


def next_month_value(month: int, shift_forward: bool = True) -> int:
    """Return shifted number of a month.

    :param month: int, number of the month in a year
    :param shift_forward: bool, Shift direction default = True, increment, except 12 -> 1
    :returns: int, next month number (shift_forward = True),
                    Previous month number (shift_forward = False)
    """
    logger.disable(__name__)
    logger.info(f"Processing <{month}>, <{type(month)}>")
    try:
        if 1 <= month <= 12:
            if shift_forward:
                if month == 12:
                    month = 1
                else:
                    month += 1
                logger.info(f"Shift forward month value to <{month}>")
            else:
                if month == 1:
                    month = 12
                else:
                    month -= 1
                logger.info(f"Shift back month value to <{month}>")
        else:
            logger.error(f"Wrong month value: <{month}>")
            month = -1

    except Exception as ex:
        logger.error(f"May be Type error?")
        raise ex

    return month
