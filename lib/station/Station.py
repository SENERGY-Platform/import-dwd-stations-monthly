#  Copyright 2024 InfAI (CC SES)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import List, Optional
from lib.util.bbox import point_in_bboxes
from import_lib.import_lib import get_logger
import requests
from datetime import date

logger = get_logger(__name__)


class Station:
    '''
    Class to store DWD station metadata
    '''
    __slots__ = ('station_id', 'date_from', 'date_to', 'height', 'lat', 'long', 'name', 'state')

    def __init__(self, station_id: str, date_from: date, date_to: date, height: int, lat: float, long: float,
                 name: str, state: str):
        self.station_id = station_id
        self.date_from = date_from
        self.date_to = date_to
        self.height = height
        self.lat = lat
        self.long = long
        self.name = name
        self.state = state


def get_stations_in_bboxes(bboxes: Optional[List[List[float]]]) -> List[Station]:
    '''
    Retrieves a list of DWD station that fit inside the bounding boxes

    :param bboxes: List of bounding boxes
    :return: List of Stations
    '''
    stations = get_stations()

    if bboxes is None:
        return stations

    selected_station_ids = []
    for station in stations:
        if point_in_bboxes(station.lat, station.long, bboxes):
            selected_station_ids.append(station)
    return selected_station_ids


def get_stations() -> List[Station]:
    '''
    Get a list of all DWD stations

    :return: List of Stations
    '''
    r = requests.get('https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/KL_Monatswerte_Beschreibung_Stationen.txt')
    if not r.ok:
        raise Exception("Could not get station list. Network OK?")
    raw = r.text
    lines = raw.splitlines()
    stations = []

    index_id, index_date_from, index_date_to, index_height, index_lat, index_long, index_name, index_state = range(8)

    lines = lines[2:]  # Remove header and separator

    for line in lines:
        fields = line.split(" ")
        while "" in fields: fields.remove("")
        while len(fields) > index_state + 1:  # names are allowed to contain spaces
            fields[index_name] += " " + fields[index_name + 1]
            del fields[index_name + 1]
        try:
            stations.append(Station(
                station_id=fields[index_id],
                date_from=date(
                    int(fields[index_date_from][0:4]),
                    int(fields[index_date_from][4:6]),
                    int(fields[index_date_from][6:8])
                ),
                date_to=date(
                    int(fields[index_date_to][0:4]),
                    int(fields[index_date_to][4:6]),
                    int(fields[index_date_to][6:8])
                ),
                height=int(fields[index_height]),
                lat=float(fields[index_lat]),
                long=float(fields[index_long]),
                name=fields[index_name],
                state=fields[index_state],
            ))
        except ValueError as e:
            logger.error(e)
            raise Exception("Could not parse station list")
    return stations


if __name__ == "__main__":
    stations = get_stations_in_bboxes(None)
    for station in stations:
        logger.info(str(station))
