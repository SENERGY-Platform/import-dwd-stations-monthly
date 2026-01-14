# Copyright 2020 InfAI (CC SES)
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

import time
from datetime import date
from typing import List

import schedule
from import_lib.import_lib import ImportLib, get_logger

from lib.station.Station import get_stations_in_bboxes
from lib.station.StationImport import StationImport

if __name__ == '__main__':
    lib = ImportLib()
    logger = get_logger(__name__)
    stationImport = StationImport(lib)

    bboxes = lib.get_config("BBOXES", None)
    if not isinstance(bboxes, List):
        logger.error("Invalid config for BBOXES will not be used")
        bboxes = None

    state, _ = lib.get_last_published_datetime()
    if state is None:
        logger.info("Import is starting fresh")
    else:
        logger.info("Import is continuing previous import")

    today = date.today()

    stations = get_stations_in_bboxes(bboxes)
    if lib.get_config("HISTORIC", False):
        if state is None or state.year < today.year - 1:
            logger.info(str(len(stations)) + " stations found in area")
            logger.info("Importing historic data of " + str(len(stations)) + " stations...")
            stationImport.import_historical(stations)
        else:
            logger.info("Skipping historic data (already done)")
    else:
        logger.info("Skipping historic data (not configured)")

    year_active_stations = [station for station in stations if station.date_to.year >= today.year - 1]

    logger.info(str(len(year_active_stations)) + " active stations this or last year")
    logger.info("Importing this years data of " + str(len(year_active_stations)) + " stations...")
    stationImport.import_recent(year_active_stations)

    logger.info("Setting schedule to run every month")
    schedule.every().day.do(stationImport.import_recent, year_active_stations)

    while True:
        schedule.run_pending()
        time.sleep(1)
