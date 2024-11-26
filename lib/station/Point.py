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

from typing import Dict

from lib.station.Station import Station


def get_message(station: Station, MO_TT, MO_TX, MO_TN, MX_TX, MX_TN, MO_SD_S, MO_RR, MX_RS) -> Dict:
    return {
        "temperature_2m_avg_celsius": MO_TT,
        "temperature_2m_avg_max_celsius": MO_TX,
        "temperature_2m_avg_min_celsius": MO_TN,
        "temperature_2m_max_celsius": MX_TX,
        "temperature_2m_min_celsius": MX_TN,
        "sun_total_hours": MO_SD_S,
        "precipiation_sum_mm": MO_RR,
        "precipiation_max_mm": MX_RS,
        "meta": {
            "name": station.name,
            "id": station.station_id,
            "lat": station.lat,
            "long": station.long,
            "height": station.height,            
        }
    }
