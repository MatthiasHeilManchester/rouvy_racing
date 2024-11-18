from config import Config
from datetime import datetime, timedelta
from collector_json import get_event_info
from common import json_date_to_datetime, nice_request, remix_parse
from enums import RouvyEventType, RouvyEventOrganizer, RouvyEventStatus
"""
That magic that finds rvy events for rvy races
"""


def find_events(race_date: datetime, route_id: str, laps: int) -> list:
    """
    Get a list of events in datetime order that match the provided values
    :param race_date: UTC Day of the race
    :param route_id: The route id  for the race
    :param laps: The number of laps
    :return: A list of events in datetime order
    """
    events: list = list()
    # search prams
    race_title: str = "rvy_racing"  # It feels bad having this as a static string here
    date_from:  str = (race_date + timedelta(days=Config.race_finder.search_back_days)).strftime("%Y-%m-%d")
    date_to:    str = (race_date + timedelta(days=Config.race_finder.search_froward_days)).strftime("%Y-%m-%d")
    event_type = RouvyEventType.RACE
    print(f'[-] Searching')

    # Updated to handel RemixJS data
    route = "events.search"
    url = (f"https://riders.rouvy.com/events/search.data?"
           f"searchQuery={race_title}&"     # Only events with rvy_racing
           f"smartTrainersOnly=true&"       # Smart Trainer only events 
           f"type={event_type.value}&"      # Only Races
           f"dateRange=custom&"
           f"dateFrom={date_from}&"
           f"dateTo={date_to}&"
           f"_routes=routes/_main.{route}")
    result = nice_request(url=url)
    remix_data = remix_parse(result.text)

    for event in remix_data[f'routes/_main.{route}']['data']['events']:
        event_start: datetime = json_date_to_datetime(event['startDateTime'])
        # Extra part day filtering
        extra_hours: int = Config.race_finder.allow_plus_n_hours
        if event_start < race_date or event_start > (race_date + timedelta(days=1, hours=extra_hours)):
            continue  # Skip events outside the allowed time window
        if event["laps"] != laps:
            continue  # Skip events that do not have the correct number of laps
        print(f'[-] Found: {event["title"]}')
        event_info: dict = get_event_info(event['id'])
        # Check the actual route id, it is not in the search results :(
        if event_info["route"]["id"] != route_id:
            print('[X] Rejected: Route incorrect')
            continue
        # All good we have an actual valid rvy_racing event...
        events.append(event_info)
    return sorted(events, key=lambda d: d['startDateTime'])


if __name__ == '__main__':
    pass
