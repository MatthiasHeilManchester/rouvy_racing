import json
import requests
from config import Config
from datetime import datetime, timedelta
from series_prcessing import get_races
from common import nice_request
from http import HTTPStatus
from enums import HTTPMethod
import common
"""
Official event creator

*************
** Warning **
*************

This is still a work in progress, I don't recommend anyone actually uses it
"""


def post_race_to_rouvy(route_id: int, race_date: datetime, offset_minutes: int, race_name: str,
                       laps: int = 1, test_mode: bool = False) -> bool:
    """
    Does the post to create an event, has a test mode that just prints the JSON
    :param route_id:
    :param race_date:
    :param offset_minutes:
    :param race_name:
    :param laps:
    :param test_mode:
    :return:
    """

    """
    Rough guess on what it will accept
    routeId: number
    title: string
    lapsCount: number().gte(1).nullish()
    disableDrafting: boolean().optional()
    smartTrainersOnly: boolean().optional()
    isMultilap: boolean().optional()
    type: enum(["RACE", "GROUP_RIDE"])
    dateTimeLocal: coerce.date() eg '2024-07-07T11:12'
    dateTimeOffset: number() in minutes, just use 0 for utc
    accessibility: enum(["PUBLIC", "PRIVATE"])
    """

    payload = {
        'type': 'RACE',
        'title': race_name,
        'dateTimeLocal': race_date.strftime('%Y-%m-%dT%H:%M'),
        'dateTimeOffset': offset_minutes,
        'accessibility': 'PUBLIC',
        'smartTrainersOnly': 'on',
        'routeId': route_id}
    if laps > 1:  # IDK if the order in important, but this it the way the site does it
        payload.pop('routeId')
        payload['isMultilap'] = 'on'
        payload['lapsCount'] = laps
        payload['routeId'] = route_id

    print(json.dumps(payload, indent=2))
    if not test_mode:
        print('[+] Creating event')
        url = f'https://riders.rouvy.com/events/setup?route={route_id}&_data=routes/_main.events_.setup.($sessionId)'
        response = nice_request(url=url, method=HTTPMethod.POST, payload=payload)
        # print(response.request.body)
        if response.status_code in [HTTPStatus.OK, HTTPStatus.NO_CONTENT]:
            print('[*] Event created')
            return True
        else:
            return False
    else:
        return True


def create_race(race_number: int, test_mode: bool = False):
    if race_number > Config.series.length or race_number < 1:
        print(f"[X] Sorry, race number {race_number} is not valid")
        return
    race_number -= 1  # 0 based lists
    race = get_races()[race_number]
    offsets: list[int] = Config.series.official_race_offsets
    tz = Config.series.official_race_timezone
    # I presumed route may change to a guid so made it a string, in needs to be in int for the post.
    route: int = int(race['route'])
    lap_count: int = race['laps']
    race_date: datetime = datetime.fromisoformat(race['date'])

    i: int = 0
    for offset in offsets:
        utc_offset = int(tz.utcoffset(race_date + timedelta(hours=offset)).total_seconds()/60)
        post_race_to_rouvy(route_id=route,
                           race_date=race_date + timedelta(hours=offset),
                           offset_minutes=utc_offset,
                           race_name=f"rvy_racing race {race['number']} {chr(ord('A') + i)}",
                           laps=lap_count,
                           test_mode=test_mode)
        i += 1


if __name__ == '__main__':
    # Create a set of races based on the config...
    # create_race(13, test_mode=True)

    # Or

    ################################################################
    # Create a single race
    ################################################################
    race_name = 'Test Race 🦄'
    race_date: datetime = datetime.fromisoformat('2024-09-24T07:00')
    route_id = 66132
    laps = 1
    test_mode = False
    ################################################################

    tz = Config.series.official_race_timezone
    utc_offset = -1 * int(tz.utcoffset(race_date).total_seconds() / 60)
    result = post_race_to_rouvy(route_id=route_id,
                                race_date=race_date,
                                offset_minutes=utc_offset,
                                race_name=race_name,
                                laps=laps,
                                test_mode=test_mode)
