from loguru import logger
import re

"""
Functions for parsing data from WhatsApp message report
"""


def get_tank_label(arg: str):
    logger.debug(f"Get tank label from:<{arg}> in {__name__}")
    parsed_groups = re.findall('[0-9]+', arg)
    logger.debug(f"parsed_groups:<{parsed_groups}>")
    parsed_groups_num = len(parsed_groups)
    if parsed_groups_num:
        label_field = parsed_groups[0]
        label_field_size = len(label_field)
        if 3 <= label_field_size <= 4:
            logger.debug(f"{label_field_size}, {label_field}")
            tank_label = label_field
            logger.debug(f"Parsed tank label:<{tank_label}>")
        else:
            logger.debug(f"Unrecognized tank_label in:<{label_field}>")
            tank_label = ''
    else:
        logger.debug(f"tank_label data format not found")
        tank_label = ''
    return tank_label


def get_provider(arg: str):
    provider = re.findall(r'[рн|рН|Рн|РН|иК|Ик|ик|ИК|касса|КАССА]{1}\w', arg)
    return provider


def get_digital(arg: str, position: int = 2):
    success_flag = False
    splatted_arg = re.split(' ', arg)
    if len(splatted_arg) > 1:
        splatted_fields = splatted_arg[position - 1]
        digital_fields = re.findall('[0-9]*[.]*[,]*[0-9]+', arg)
        logger.debug(f"digital_fields:{digital_fields}, {len(digital_fields)}")
        if len(digital_fields) > 1:
            field2convert = digital_fields[position - 1]
            logger.debug(
                f"Get field2convert on position <{position}> from:<{splatted_fields}> parsed as <{field2convert}>")
            try:
                digital: float = float(field2convert)
                logger.debug(f"Successful transform to:<{digital}>")
                success_flag = True
            except:
                logger.error(f"Transform error <{field2convert}> in <{arg}>")
        else:
            logger.debug(f"No enough digital fields in report string:\n{digital_fields}")
    else:
        logger.error(f"Wrong data format in arg:\n<{arg}>")

    return digital if success_flag else -1
