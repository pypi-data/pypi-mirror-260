import re
from datetime import datetime
import pandas as pd

from loguru import logger

from ownlib.class_whatsapp_message import WhatsAppMessage
from ownlib.txt_lib import string_transform, SPACE_CHAR, EMPTY_STR

logger.disable(__name__)
logger.info(f"Importing module...")

pd.set_option('max_rows', 1000)
# pd.set_option('max_colwidth', 400)
# pd.describe_option('max_rows')

clr_rules = {'\xa0': EMPTY_STR,
             '\n': EMPTY_STR,
             '\u200e': EMPTY_STR,
             '*': EMPTY_STR,
             '(': EMPTY_STR,
             ')': EMPTY_STR
             }

DATETIME_INIT = datetime(1900, 1, 1, 0, 0, 0, 0)

REFUELING_LIMIT: tuple = (35, 1200)
MINIMUM_VOLUME = 2000.0
MAXIMUM_VOLUME = 10000.0
MINIMUM_MONEY = 40.0
MAXIMUM_MONEY = 500000.0
LARGEST_PRICE = 100.0

delivery_price = 0.0


def get_tank_status(data_field: str) -> str:
    assert type(data_field) == str
    logger.disable(__name__)

    lorry_same = len(data_field) == 3
    trailer_same = len(data_field) == 4

    if lorry_same:
        tank_status = 'Lorry'
    elif trailer_same:
        tank_status = 'Trailer'
    else:
        tank_status = 'WrongKind'
    return tank_status


def tank_data(arg: str):
    status = get_tank_status(arg)
    name = arg
    return name, status


def checked_refueling(arg: int, refueling_limit: tuple = REFUELING_LIMIT) -> int:
    arg_min, arg_max = refueling_limit
    if arg_min < arg <= arg_max:
        return arg
    else:
        return -1


def get_vehicle_id(tank: str, id_df: pd.DataFrame) -> str:
    # logger.enable(__name__)
    logger.disable(__name__)
    logger.debug(f"Find id for tank <{tank}>")
    vehicle_id = [EMPTY_STR]
    id_series = id_df.iloc[:, 0]
    try:
        vehicle_id = [field.strip() for field in id_series if tank == re.findall('[0-9]\w+', field)[0]]  # WTF?
        logger.debug(f"len: <{len(vehicle_id)}>, <{vehicle_id}>")
        if len(vehicle_id) > 1:
            logger.warning(f"Multiply result for {tank}")
        elif len(vehicle_id):
            logger.success(f"ID for {tank} = {vehicle_id}")
        else:
            vehicle_id = [EMPTY_STR]
            logger.warning(f"Pattern {tank} not found")
    except Exception as vehicle_ex:
        logger.error(f"Error with {tank}, {vehicle_ex=}")
    # logger.disable(__name__)
    return vehicle_id[0]


def get_vehicle_cards(key_pattern: str, data_df: pd.DataFrame) -> dict:
    """Return cards number after filtering column [0]"""
    # logger.enable(__name__)
    logger.disable(__name__)
    logger.debug(f"pattern: <{key_pattern}>")

    result_row = data_df.index[data_df.iloc[:, 0].values == key_pattern]
    if len(result_row):
        logger.debug(f"result_row:<{result_row}>")
        cards = {'rn': data_df.iloc[result_row, 1].tolist()[0],
                 'ic': data_df.iloc[result_row, 2].tolist()[0]
                 }
        logger.debug(f"cards: <{cards}>")
    else:
        cards = {}
        logger.error(f"***************SOMETHING WRONG*************")
    # logger.disable(__name__)
    return cards


def getRefueling(arg: str) -> dict:
    logger.disable(__name__)
    # logger.enable(__name__)
    logger.debug(f"get refueling data from <{arg}>")

    patterns_with_digital = re.findall(r'\d\w+', arg)
    logger.debug(f"blocks_with_digital = {patterns_with_digital}")

    digital_only_patterns = [re.findall(r'\d+', i) for i in patterns_with_digital]
    logger.debug(f"digital_only_patterns = {digital_only_patterns}")

    if len(patterns_with_digital) >= 2:
        logger.debug(
            f"Successful get refueling data from a string:\npatterns_with_digital:<{patterns_with_digital}>\n\
            digital_only_patterns:<{digital_only_patterns}>.")
        return dict(tank=digital_only_patterns[0][0],
                    volume=int(digital_only_patterns[1][0])
                    )
    else:
        logger.warning(
            f"Can`t to find refueling data in:\n{arg}\npatterns_with_digital:<{patterns_with_digital}>\n\
            digital_only_patterns:<{digital_only_patterns}>")
        return {}


def repRowInit() -> dict:
    """
    Initialize parsed row data structure

    :returns: dict
    """
    initdatetime = datetime(1900, 1, 1, 0, 0, 0, 0)

    return dict(MsgKind=EMPTY_STR,
                DateTime=initdatetime,
                Sender=None,
                Sender_1C=EMPTY_STR,
                Tank=EMPTY_STR,
                TankStatus=EMPTY_STR,
                Source='own',
                Refueling=0.0,
                Price=0.0,
                Cost=0.0,
                MsgTxt=EMPTY_STR,
                Card=EMPTY_STR,
                DropFlag=False
                )


"""
Functions for parsing data from WhatsApp message report
"""


def get_tank_field(arg: str) -> str:
    """
    Get first digit part (3 <= len(tank_label) <= 4) from arg

    :param arg: str, WhatsApp message body
    :returns: str, contains digital part of a vehicle registration number
    """
    logger.disable(__name__)
    parsed_groups: list = re.findall('[0-9]+', arg)
    logger.debug(f"parsed_groups:<{parsed_groups}>")
    parsed_groups_num: int = len(parsed_groups)
    if parsed_groups_num:
        checking_field = parsed_groups[0]
        checking_field_size: int = len(checking_field)
        if 3 <= checking_field_size <= 4:
            logger.debug(f"{checking_field_size}, {checking_field}")
            tank_field: str = checking_field
            logger.debug(f"Parsed tank label:<{tank_field=}>")
        elif 'приход | коррекция' in arg.lower():
            logger.debug(f"Set OWN_TANK flag:<{arg=}>")
            tank_field: str = 'OWN_TANK'
        else:
            logger.debug(f"Unrecognized tank_label in:<{checking_field=}>")
            tank_field = EMPTY_STR
    else:
        logger.debug(f"tank_label data format not found, {parsed_groups_num=}")
        tank_field = EMPTY_STR
    return tank_field


def get_provider_field(arg: str) -> str:
    """
    Find in arg one of preset pattern [р//н|рн|рН|Рн|РН|иК|Ик|ик|ИК|касса|КАССА]

    :param  arg: WhatsApp message body
    :returns: string.lower(), contained one of founded patterns
    """
    provider_field = re.findall(r'[р/н|рн|рН|Рн|РН|иК|Ик|ик|ИК|касса|КАССА]+\w', arg)  # (!) CHECK р/н
    return str(provider_field).lower()


def get_digital(arg: str, position: int = 2) -> float:
    """
    Return float(digital group in  arg) try to find it on '123 ->345.56<- 789' position (like 345.56 in default case)

    :param  arg: str, WhatsApp message body
    :param position: int, digit group number in arg
    :returns: float(digital), if successful, or -1 if else
    """
    logger.disable(__name__)
    success_flag: bool = False
    splatted_arg: list = re.split(SPACE_CHAR, arg)
    splatted_arg_size: int = len(splatted_arg)
    logger.debug(f"Splat <{splatted_arg_size}> groups {splatted_arg}")
    digital_fields = re.findall('[0-9]*[.]*[,]*[0-9]+', arg)
    digital_fields_num = len(digital_fields)
    logger.debug(f"Got <{digital_fields_num}> groups {digital_fields}")
    digital: float = 0.0
    # if splatted_arg_size > position - 1:
    try:
        splatted_fields = splatted_arg[position - 1]
        # digital_fields = re.findall('[0-9]*[.]*[,]*[0-9]+', splatted_fields)
        logger.debug(f"digital_fields:{digital_fields}, {len(digital_fields)}")
        # if len(digital_fields) > 1:
        field2convert: str = digital_fields[position - 1]
        field2convert = field2convert.replace(',', '.')
        logger.debug(f"Get field2convert on position <{position}> \
        from:<{splatted_fields}> parsed as <{field2convert}>")
        try:
            digital: float = float(field2convert)
            logger.debug(f"Successfully transform to:<{digital}>")
            success_flag = True
        except:
            logger.error(f"Transform error <{field2convert}> in <{arg}>")
    except IndexError:
        logger.debug(f"No enough digital fields in report string:\n{digital_fields}")
    except:
        logger.error(f"Wrong data format in arg:\n<{arg}>")

    return digital if success_flag else -1


def get_own_price(message_: str) -> dict:
    logger.disable(__name__)
    result_dict = {}

    if 'приход' in message_.lower():
        fuel = get_digital(message_, 1)
        money = get_digital(message_, 2)
        if MINIMUM_VOLUME < fuel < MAXIMUM_VOLUME:
            result_dict['volume'] = fuel
            if MINIMUM_MONEY < money < MAXIMUM_MONEY:
                if money <= LARGEST_PRICE:
                    result_dict['price'] = money
                    logger.info(f"[+] Direct price setting {money=}")
                else:
                    result_dict['price'] = money / fuel
                    logger.info(f"[+] Took price from total / volume, {money=}")
            else:
                logger.error(f"[!] Wrong price data! {money=}")
        else:
            logger.error(f"[!] Wrong volume data! {fuel=}")

    return result_dict


def get_refueling_source(buff: str, default_source: str = 'own') -> str:
    logger.disable(__name__)
    if 'рн' in buff:
        logger.debug(f"Set ROSNEFT source flag")
        source = 'rn'
    elif 'ик' in buff:
        logger.debug(f"Set INFORCOM source flag")
        source = 'ic'
    elif 'касса' in buff:
        logger.debug(f"Set CASH source flag")
        source = 'cash'
    else:
        logger.debug(f"No outside source flags found. leave OWN source status")
        source = default_source

    return source


def get_refueling_card(vehicle: str, refueling_source: str, vehicle_data) -> str:
    # logger.enable(__name__)
    logger.disable(__name__)
    card_index = vehicle_data.index[vehicle_data.iloc[:, 0].values == vehicle]
    if len(card_index):
        logger.debug(f"card_index:<{card_index.values[0]}>")
        card_info = vehicle_data.iloc[card_index, ][refueling_source].values[0]
        logger.debug(f"<{card_info=}>")
    else:
        logger.error(f"Error with <{vehicle=}, <{card_index=}>")
        card_info = 'unknown'
        # logger.disable(__name__)
    return card_info


def get_messages_df(messages: list) -> pd.DataFtrame:
    parsed_dataset = []
    #    logger.disable(__name__)
    #    logger.enable(__name__)

    datetime_cached = DATETIME_INIT
    sender_cached = EMPTY_STR

    for message in messages:
        processed_message = WhatsAppMessage(message)

        if processed_message.master:
            datetime_cached = processed_message.message_datetime
            sender_cached = processed_message.sender
            logger.debug(f"Master message, cache refreshed.")
        elif processed_message.status == 'continuation':
            processed_message.message_datetime = datetime_cached
            processed_message.sender = sender_cached
            logger.debug(f"Load datetime and sender data from master message.")

        cleared_message = string_transform(processed_message.message, clr_rules)

        logger.debug(f"{type(processed_message.message_datetime)=}")
        parsed_data = dict(date=processed_message.message_datetime,
                           year=processed_message.message_datetime.year,
                           month=processed_message.message_datetime.month,
                           sender=processed_message.sender,
                           message=cleared_message,
                           status=processed_message.status,
                           is_master=processed_message.master,
                           source=processed_message.source
                           )

        parsed_dataset.append(parsed_data)
    logger.enable(__name__)
    result_df = pd.DataFrame(data=parsed_dataset, index=None)

    return result_df


def make_data_filename(df, date_field: str = 'DateTime', name_prefix: str = 'WhatsAppParsed_FROM_') -> str:
    part_from = '_FROM_' + str(df[date_field].min()).split(SPACE_CHAR)[0]
    part_to = '_TO_' + str(df[date_field].max()).split(SPACE_CHAR)[0]
    made_data = '_MADE<' + str(datetime.today()).split(SPACE_CHAR)[0]
    ext_str = '>.pkl'

    return EMPTY_STR.join([name_prefix,
                           part_from,
                           part_to,
                           made_data,
                           ext_str])
