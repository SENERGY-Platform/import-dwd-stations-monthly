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
from typing import List, Union, Tuple


def point_in_bbox(lat: float, long: float, bbox: List[float]) -> bool:
    '''
    Checks if the point is in the bbox
    :param lat: Point lat
    :param long: Point long
    :param bbox: The bounding box as [min Longitude, min Latitude, max Longitude, max Latitude]
    :return: True, if point is the bbox, False otherwise
    '''
    return bbox[0] <= long <= bbox[2] and bbox[1] <= lat <= bbox[3]


def point_in_bboxes(lat: float, long: float, bboxes: List[List[float]]) -> bool:
    '''
    Checks if the point is in at least one bbox
    :param lat: Point lat
    :param long: Point long
    :param bboxes: List of bboxes
    :return: True, if point is in at least one bbox, False otherwise
    '''
    for bbox in bboxes:
        if point_in_bbox(lat, long, bbox):
            return True
    return False
