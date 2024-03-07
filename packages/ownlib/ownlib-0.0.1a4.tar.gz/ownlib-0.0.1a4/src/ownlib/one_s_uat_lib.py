from dataclasses import dataclass
from datetime import datetime
import pandas as pd


@dataclass
class TripInfo:
    _source_string: str

    def __post_init__(self):
        __trip_data_list = self._source_string.split(';')
        self.id = __trip_data_list[0].split()[0].strip(' :;')
        self.date = datetime.strptime(__trip_data_list[0].split()[1].split('-')[0], '%d.%m.%Y').date()
        self.plate = __trip_data_list[1].strip(' ;')
        self.routes = [route.strip() for route in __trip_data_list[2:]]


def ticket_info_parse(df: pd.DataFrame, ticket_label: str = 'Ticket_info') -> pd.DataFrame:
    id_buffer = []
    date_buffer = []
    plate_buffer = []
    routes_buffer = []

    driver_buffer = []

    for note in df[ticket_label]:
        if ';' in note:
            trip_data = TripInfo(note)
            id_buffer.append(trip_data.id)
            date_buffer.append(trip_data.date)
            plate_buffer.append(trip_data.plate)
            routes_buffer.append(trip_data.routes)
            driver_buffer.append(None)
            del trip_data
        else:
            routes_buffer.append(None)
            id_buffer.append(None)
            date_buffer.append(None)
            plate_buffer.append(None)
            driver_buffer.append(note.strip())

    df['Id'] = pd.Series(id_buffer)
    df['Date'] = pd.Series(date_buffer, dtype='datetime64[ns]')
    df['Plate'] = pd.Series(plate_buffer)
    df['Routes'] = pd.Series(routes_buffer)
    df['Driver'] = pd.Series(driver_buffer)

    for row in df.itertuples():
        if row.Driver is None:
            df.loc[row.Index, 'Driver'] = df.loc[row.Index + 1, 'Driver']

    return df.iloc[::2, :].reset_index(drop=True).copy()
