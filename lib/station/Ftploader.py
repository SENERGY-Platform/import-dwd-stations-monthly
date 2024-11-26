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

import csv
import io
import zipfile
from ftplib import FTP
from typing import List, Optional, Callable, Tuple

import requests
from import_lib.import_lib import get_logger

from lib.station.Station import Station

logger = get_logger(__name__)

DWD_HOST = "opendata.dwd.de"
DWD_RECENT_PATH = "climate_environment/CDC/observations_germany/climate/monthly/kl/recent/"
DWD_HISTORICAL_PATH = "climate_environment/CDC/observations_germany/climate/monthly/kl/historical/"
DWD_RECENT_URL = "https://" + DWD_HOST + "/" + DWD_RECENT_PATH
DWD_HISTORICAL_URL = "https://" + DWD_HOST + "/" + DWD_HISTORICAL_PATH


def get_recent(station: Station) -> Optional[List[csv.DictReader]]:
    '''
    Downloads recent data (current year) of a station

    :param station: DWD station
    :return: csv.DictReader to read the data or None if no data was available
    '''
    r = __get_with_url(DWD_RECENT_URL + "monatswerte_KL_" + station.station_id + "_akt.zip")
    if r is None:
        logger.error("No recent values for station with id " + station.station_id + ". Station still active?")
        return None
    return r


def get_historical(stations: List[Station], callback: Callable[[Station, List[csv.DictReader]], any] = None) \
        -> Optional[List[Tuple[Station, List[csv.DictReader]]]]:
    '''
    Downloads all historical data of a list of stations. You might provide a callback in order to receive smaller
    chunks of data (highly recommended). Return values of the callback will be ignored.

    :param stations: List of DWD stations
    :param callback: Callable that receives a station and a List of csv.DictReader for further processing.
    The List might be a sublist of all historic files of that station, but the callback will be called again if more
    data is available.
    :return: List of Tuples of a station and a List of csv.DictReader to read the data or None if the callback received
    the data already.
    '''
    files = __get_files_of_dir(DWD_HISTORICAL_PATH)
    station_readers = []
    for file in files:
        for station in stations:
            if file.count("KL_" + station.station_id):
                r = __get_with_url(DWD_HISTORICAL_URL + file)
                if callback is None and r is not None:
                    station_readers.append((station, r))
                elif r is not None:
                    callback(station, r)
    if callback is None:
        return station_readers
    return None


def __get_with_url(url: str) -> Optional[List[csv.DictReader]]:
    r = requests.get(url)
    if not r.ok:
        return None
    return __read_zipped_txts(r.content)


def __read_zipped_txts(zip: bytes) -> List[csv.DictReader]:
    with zipfile.ZipFile(io.BytesIO(zip)) as thezip:
        for zipinfo in thezip.infolist():
            if not zipinfo.filename.startswith('produkt_klima_monat_'):
                continue
            with thezip.open(zipinfo) as thefile:
                b_lines = thefile.readlines()
                s_lines = []
                for b_line in b_lines:
                    s_lines.append(b_line.decode().replace(" ", ""))
                yield csv.DictReader(s_lines, delimiter=";")
                thefile.close()
                thezip.close()


def __get_files_of_dir(dir: str, suffix: str = None) -> List[str]:
    client = FTP(DWD_HOST)
    client.login()
    client.cwd(dir)
    files = client.nlst()
    client.close()
    if suffix is None:
        return files
    filteredFiles = []
    for f in files:
        if f.endswith(suffix):
            filteredFiles.append(f)
    client.close()
    filteredFiles.sort()
    return filteredFiles
