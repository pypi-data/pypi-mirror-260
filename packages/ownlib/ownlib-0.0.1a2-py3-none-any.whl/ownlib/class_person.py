from dataclasses import dataclass

from loguru import logger

logger.disable(__name__)


# noinspection SpellCheckingInspection
@dataclass
class PersonName:
    """
    Object for storage and tiny manipulating person name`s data\n
    Set name, first, middlename, lastname attribs,\n
    TODO FIX unprocessing case with 'Doe J.J.' - like buffer!
    Strip extra spaces,\n
    Titling first characters,\n
    Set order in fullname via order (f-irst, m-iddlle, l-ast), default = 'lfm'.\n

    Example:\n PersonName(' John   smith Dou  ', 'fml')\n
    >> Example.fullname = 'John Smith Dou '
    """
    __init_buff: str = ''
    order: str = 'lfm'

    def __post_init__(self):
        self.orders = {'lfm': (1, 2, 0),
                       'fml': (0, 1, 2)}
        names = self.__init_buff.strip().title().split()
        self.name = ' '.join(names)
        self.firstname, self.middlename, self.lastname, self.fullname = '', '', '', ''
        names_quantity = len(names)

        if not names:
            pass
        elif names_quantity == 3:
            try:
                self.firstname, self.middlename, self.lastname = (names[idx] for idx in self.orders[self.order])
                self.fullname = ' '.join((names[idx] for idx in self.orders[self.order]))
                logger.success(f"Parsed person name: {self.fullname}")
            except:
                logger.error(f"[!] {type(self)}, Unknown order claiming: <{self.order}>!")
        # TODO Temporary - in case 2 name fields. Think about optimization!
        elif names_quantity == 2:
            self.fullname = self.name
        else:
            logger.error(f"[!] Incompartible person name information format in {type(self)}!")

        def _get_initial(namefield: str) -> str:
            if namefield:
                _result = namefield[0] + '.'
            else:
                _result = ''
            return _result

        self.initial_firstname = _get_initial(self.firstname)
        self.initial_middlename = _get_initial(self.middlename)


class Person(PersonName):
    """
    TODO FIX unprocessing case with 'Doe J.J.' - like buffer!
    """
    logger.debug(f"Some define log from Person")
