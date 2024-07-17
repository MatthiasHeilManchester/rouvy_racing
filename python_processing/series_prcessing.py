import json
import operator
from config import Config, IsoDow
from common import json_date_to_datetime
from pathlib import Path
from collector_json import (get_route_info, get_event_results, get_challenges,
                            route_challenge_dict, convert_user_data_to_json)
from datetime import datetime, date, timedelta
from event_finder import find_events
from jinja2 import Environment, FileSystemLoader
POINTS = Config.series.points
"""
Less "Bolshy"?

Handles all the race processing and html generation
"""


def __generate_races() -> list:
    """
    Internally used by init_series() plan out the race calendar based and feed races.json
    :return: A race list for races.json
    """
    series: list = list()
    start: date = Config.series.start_date
    race_days = Config.series.race_days
    assert IsoDow(start.isoweekday()) in race_days, \
        f"The start date's day, must be a race day {list(map(lambda x: f'{x}', race_days))}"
    race_date: date = start
    last_race_day: IsoDow = IsoDow(start.isoweekday())
    for i in range(int(Config.series.length)):
        race_number = i + 1
        path = Path(Config.series.series_path, f'race{race_number:05}')
        series.append({'number': race_number,
                       'route': Config.series.route(i),
                       'laps': Config.series.lap_count(i),
                       'date': str(race_date),
                       'name': f"Race {race_number} : {race_date.strftime('%d %b %Y')}",
                       'day': race_date.isoweekday(),
                       'path': str(path)})
        next_race_day = min((i for i in race_days if i > last_race_day), default=min(race_days))
        if next_race_day == last_race_day:
            incro = 7
        else:
            incro = (next_race_day - last_race_day) % 7
        race_date = race_date + timedelta(incro)
        last_race_day = next_race_day
    return series


def get_races() -> list:
    """
    Loads and returns the race list.
    :return: Race list
    """
    race_file: Path = Path(Config.series.series_path, 'races.json')
    return json.load(race_file.open(mode='r', encoding='utf-8'))


def init_races():
    """
    Initialise all races that are not TBA
     - Create race folder if needed
     - Collect route information from Rouvy and dump it into route.json
    """
    print(f"[*] Initialising any new races")
    races = get_races()
    race: dict
    for race in races:
        route_id: str = race['route']
        if route_id == 'TBA':
            print(f'[-] {race["name"]} route TBA')
            continue
        race_path = Path(race['path'])
        race_path.mkdir(exist_ok=True)
        route_file = Path(race_path, 'route.json')
        if route_file.exists():
            # print(f'[-] {race["name"]} already initialised')
            pass
        else:
            route: dict = get_route_info(route_id)
            json.dump(route, route_file.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print(f'[*] {race["name"]} initialised')


def init_series():
    """
    Initialise and extend / update races.json as required based on .series.env
    """
    races: list = __generate_races()
    race_file: Path = Path(Config.series.series_path, 'races.json')
    if not race_file.exists():
        # All new just dump out the generated race schedule
        json.dump(races, open(race_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'[*] "{Config.series.name}" initialised')
        return
    # races.json exists, lets see if it needs updating
    update_required: bool = False
    # Append anything new
    current_races: list = get_races()
    current_races_len: int = len(current_races)
    for i in range(0, Config.series.length):
        if i >= current_races_len:  # A new race, just add it
            current_races.append(races[i])
            update_required = True
            continue
        gen_race: dict = races[i]
        # See if we need to update anything
        if current_races[i]['route'] == 'TBA' and gen_race['route'] != 'TBA':
            current_races[i]['route'] = gen_race['route']
            current_races[i]['laps'] = gen_race['laps']
            update_required = True

    # Do the update if we need to
    if update_required:
        json.dump(current_races, open(race_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'[-] "{Config.series.name}" updated')
    else:
        print(f'[-] "{Config.series.name}" up to date')


def collect_event_data(race_number: int):
    """
    If results.json exists this race is over and the leaderboard collected, no additional action will be taken.
    If results.json does not exist:
     - Search for all official and non-official events that match the race parameters.
     - Replace events.json with the new / current data
    If results.json exists this race is over and the leaderboard collected
    Additionally if all events are complete, collect the results and save it to results.json
    :param race_number: The race number to process
    """
    race: dict = get_races()[race_number-1]
    race_path: Path = Path(race['path'])
    race_path.mkdir(exist_ok=True)  # should already exist but you never know
    event_file: Path = Path(race_path, f'events.json')
    results_file: Path= Path(race_path, f'results.json')
    if results_file.exists():
        print(f'[-] Race {race["name"]} complete and results already collected')
        return
    print(f'[-] Collecting event data for {race["name"]}')
    # Collect Complete and planned events
    events = (find_events(datetime.fromisoformat(race['date']), race['route'], race['laps'], finished=False)
              + find_events(datetime.fromisoformat(race['date']), race['route'], race['laps'], finished=True))
    json.dump(events, open(event_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    # Is it time to start collecting event leaderboards?
    last_event_offset = timedelta(hours=24 + Config.race_finder.allow_plus_n_hours)
    last_event_date = datetime.fromisoformat(race['date']) + last_event_offset

    # If we are < 1 hour past the start time of the last possible event return
    if datetime.utcnow() < (last_event_date + timedelta(hours=1)):
        print(f'[*] {race["name"]} not ready for collection, based on time')
        return

    # If we have an event that is not 'FINISHED' return
    if max([e['status'] != 'FINISHED' for e in events]):
        print(f'[*] {race["name"]} not ready for collection, all events not yet finished')
        return

    # Nice, now that wre are here all events are 'FINISHED' lets collect the results
    results = list()
    event: dict
    for event in events:
        if event['registrationsCount'] == 0:
            # skip events if the muppet that created it de-registered and was the only rider
            continue
        results.append({event['id']: get_event_results(event['id'])})
    json.dump(results, open(results_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def format_race_date(val: str):
    """
    Custom formatting used in JINJA templates
    :param val: An empty string or a JSON data structure
    :return: A formated time string
    """
    if str(val).strip() == '':
        return ''
    dt = json_date_to_datetime(val)
    return dt.strftime('%H:%M') + ' (UTC)'


def __combine_everything_for_jinja_template() -> dict:
    """
    Combines all the things into a single dictionary for JINJA templates.
    :return: JINJA template data
    """
    races: list = get_races()
    reverse_races: list = sorted(races, key=lambda _: _['number'], reverse=True)
    race: dict
    for race in reverse_races:
        # Add route info
        route_file: Path = Path(race['path'], 'route.json')
        route: dict = json.load(open(route_file, 'r', encoding='utf-8'))
        race['route'] = route['route']

        # Add event info
        events_file: Path = Path(race['path'], 'events.json')
        if events_file.exists():
            events = sorted(json.load(open(events_file, 'r', encoding='utf-8')), key=lambda _: _['startDateTime'])
        else:
            # Lost events due to Rouvy update
            events = [{'id': '',
                       'title': 'Events have been lost due to Rouvy update',
                       'registrationsCount': -1,
                       'author': {'username': Config.series.official_authors[0]}}]

        official_events = [x for x in events if x['author']['username'] in Config.series.official_authors]
        user_contribute_events = [x for x in events if x['author']['username'] not in Config.series.official_authors]
        race['events'] = official_events
        race['user_contribute_events'] = user_contribute_events

        # Add race leaderboard
        leaderboard_file = Path(race['path'], f'leaderboard.json')
        if leaderboard_file.exists():
            race['processed'] = True
            results = json.load(open(leaderboard_file, 'r', encoding='utf-8'))
            race['results'] = results
        else:
            race['processed'] = False

    series_leaderboard_file = Path(Config.series.series_path, 'series_leaderboard.json')
    series_leaderboard = json.load(open(series_leaderboard_file, 'r', encoding='utf-8'))
    template_data: dict = {'series_leaderboard': series_leaderboard,
                           'races': reverse_races}
    return template_data


def generate_all_races_html():
    """
    Create all_races_in_series.html via JINJA template
    """
    template_data: dict = __combine_everything_for_jinja_template()
    environment = Environment(autoescape=True, loader=FileSystemLoader("templates", encoding='utf-8'))
    environment.filters['parse_ts'] = format_race_date
    template = environment.get_template("all_races_in_series.jinja")
    template.globals['now'] = datetime.utcnow
    template.globals['race_series'] = Config.series.name
    # TODO: Set this path via settings, not hard coded
    all_race_file = Path('..', 'generated_html', 'rvy_racing', 'all_races_in_series.html')
    all_race_file.write_text(template.render(template_data), encoding='utf-8')


def generate_league_table_html():
    """
    Create league_table.html via JINJA template
    """
    template_data: dict = __combine_everything_for_jinja_template()
    environment = Environment(autoescape=True, loader=FileSystemLoader("templates", encoding='utf-8'))
    environment.filters['parse_ts'] = format_race_date
    template = environment.get_template("league_table.jinja")
    template.globals['now'] = datetime.utcnow
    template.globals['race_series'] = Config.series.name
    # TODO: Set this path via settings, not hard coded
    all_race_file = Path('..', 'generated_html', 'rvy_racing', 'league_table.html')
    all_race_file.write_text(template.render(template_data), encoding='utf-8')


def create_race_leaderboard(race_number: int):
    """
    Finds each user's best time over every event in a race and allocates the appropriate points
    :param race_number: The race number to process
    """
    races: list = get_races()
    race: dict = races[race_number-1]
    race_path: Path = Path(race['path'])
    agg_results = list()
    results_file = Path(race_path, f'results.json')
    if not results_file.exists():
        print(f'[*] No results for {race["name"]} currently available')
        return
    results: list = json.load(results_file.open(mode='r', encoding='utf-8'))
    user_file = Path(Config.series.series_path, f'user_data.json')
    users: dict = json.load(user_file.open(mode='r', encoding='utf-8'))
    event: dict
    for event in results:
        event_id: str = list(event.keys())[0]
        rider: dict
        for rider in event[event_id]['leaderboard']:
            if rider['time'] == '0':
                rider['time'] = rider['userSessionStatus']
            agg_results.append(rider)

    # agg results and get best time
    best_results = list()
    rider_check = list()
    agg_position = 1
    for x in sorted(agg_results, key=lambda d: float(d['timeSeconds']) if float(d['timeSeconds']) != 0 else 1e999):
        if x['userName'] in rider_check or x['userName'] not in users:
            continue
        rider_check.append(x['userName'])
        x['aggPosition'] = agg_position
        points = 0
        # Allocate points for the rank
        if x["userSessionStatus"] == 'finished' and len(POINTS) > agg_position:
            points = POINTS[agg_position-1]

        agg_position += 1
        user_info: dict = users[x['userName']]

        x.pop('position', None)
        best_results.append({**x, 'rvy_points': points, **user_info})

    if Config.series.include_dnr:
        # Add in all rvy users that did not register
        for x in users:
            if x in rider_check:
                continue
            # fake up a row for them
            user_info: dict = users[x]
            best_results.append({'userName': user_info['rvy_rouvy_name'],
                                 'time': 'DNR',
                                 'team': '',
                                 'timeSeconds': 0,
                                 'rvy_points': 0,
                                 'countryCode': user_info['rouvy'].get('countryCode', 'XX'),
                                 'userSessionStatus': 'DNR',
                                 'aggPosition': agg_position,
                                 **user_info})
            agg_position += 1

    leaderboard_file: Path = Path(race_path, "leaderboard.json")
    json.dump(best_results, leaderboard_file.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)


def create_series_leaderboard():
    """
    Creates a series_leaderboard.json file from all the race leaderboard.json files
    """
    # Things that are not useful in a series_leaderboard
    remove_list = ['time', 'timeSeconds', 'userSessionStatus', 'aggPosition', 'avgWattKg', 'avgSpeedmps']
    league_table = dict()
    race: dict
    for race in sorted(get_races(), reverse=True, key=lambda d: d['number']):  # Reversed to get most current user Info
        leaderboard_file = Path(race['path'], 'leaderboard.json')
        if not leaderboard_file.exists():
            continue
        leaderboard: list = json.load(leaderboard_file.open(mode='r', encoding='utf-8'))
        for lb_result in leaderboard:
            race_complete = 0
            if lb_result["userSessionStatus"] == 'finished':
                race_complete = 1

            for pop in remove_list:
                lb_result.pop(pop, None)

            if lb_result['userName'] in league_table and league_table[lb_result['userName']]['raceCompleteCount'] > 0:
                league_table[lb_result['userName']]['rvy_points'] += lb_result.get('rvy_points', 0)
                league_table[lb_result['userName']]['raceCompleteCount'] += race_complete
            else:
                league_table[lb_result['userName']] = {'raceCompleteCount': race_complete, **lb_result}

    league_list = list()
    for lb_result in league_table:
        league_list.append(league_table[lb_result])

    ranked_league_list = list()
    rank = 1
    last_rank = -1
    last_points = -1
    for lb_result in sorted(league_list, reverse=True, key=lambda d: float(d['rvy_points'])):
        allocated_rank = rank
        if last_points != lb_result['rvy_points']:
            last_points = lb_result['rvy_points']
            last_rank = rank
        else:
            allocated_rank = last_rank
        ranked_league_list.append({'rank': allocated_rank, **lb_result})
        rank += 1

    league_lb_file: Path = Path(Config.series.series_path, 'series_leaderboard.json')
    json.dump(ranked_league_list, league_lb_file.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)


def create_iso3166_1_leaderboard():
    """
    Creates a leaderboard based on the ISO3166-1 A-2 Country codes, possibly creating an international incident
    """
    series_lb_file: Path = Path(Config.series.series_path, 'series_leaderboard.json')
    series_lb: list = json.load(series_lb_file.open(mode='r', encoding='utf-8'))
    league_of = dict()
    for league_row in series_lb:
        if int(league_row['rvy_points']) == 0:
            continue
        cc: str = league_row['countryCode']
        points: int = int(league_row['rvy_points'])
        if cc in league_of:
            league_of[cc] = league_of[cc] + points
        else:
            league_of[cc] = points

    _list: list = [{'cc': k, 'points': v} for k, v in league_of.items()]
    sorted_iso_lb: list = sorted(_list, key=lambda _x: int(_x['points']), reverse=True)

    iso_lb_file: Path = Path(Config.series.series_path, 'iso3166_1_leaderboard.json')
    json.dump(sorted_iso_lb, iso_lb_file.open('w', encoding='utf-8'), ensure_ascii=False, indent=2)


def update_races_with_challenge():
    """
    Updates races.json with any matching challenges for when the race is to be run
    """
    # YOLO
    # TODO: This will (most likely) fail if rouvy stage >1 challenge on the same route at the same time
    #       Add some code to deal with this possibility
    races: list = get_races()
    challenges: dict = route_challenge_dict(get_challenges())
    updated = False
    for race in races:
        if 'challenge' in race:  # Looks like we already found a challenge for this race
            continue
        route: str = race['route']
        race_date: datetime = datetime.fromisoformat(race['date'])
        if route in challenges:
            challenge: dict = challenges[route]
            challenge_start = json_date_to_datetime(challenge['startDateTime'])
            challenge_end = json_date_to_datetime(challenge['endDateTime'])
            if challenge_start <= race_date <= challenge_end:
                updated = True
                print(f'New Challenge found for race [{race["name"]}] route {route} - {challenge["title"]}')
                race['challenge'] = challenge
    if updated:
        series_file = Path(Config.series.series_path, 'races.json')
        json.dump(races, open(series_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def create_user_data_json_file():
    """
    Converts user_data.csv to JSON and merges in information from Rouvy
    """
    json_user_data_file: Path = Path(Config.series.series_path, 'user_data.json')
    if not json_user_data_file.exists():
        user_data: dict = convert_user_data_to_json()
        # Move the users that we can not find on Rouvy to the end of the dictionary
        sorted_user_data: dict = dict()
        sorted_keys = sorted(user_data, key=lambda user: user_data[user]['rouvy'].get('error', ''))
        for k in sorted_keys:
            sorted_user_data[k] = user_data[k]
        json.dump(sorted_user_data, open(json_user_data_file, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # Based on the `.series.env` file loaded
    # Create directory and races.json
    # routes will be TBA unless otherwise specified in the `.series.env` file
    # This will only be created if it does not exist
    init_series()
    # It would be a good idea to now check races.json looks correct

    # create a json version of user_data.csv
    create_user_data_json_file()

    # Collect route.json and put in it a race folder
    # TBA races are ignored
    init_races()

    # Add the first challenge we find that matches to races.json
    update_races_with_challenge()

    # Collect events and if the event is completed the leaderboard
    # races 1 to 5 have been lost in the Rouvy updates
    # leaderboard.json files have been backfilled from rvy_racing html for races 1->5
    for _race_number in range(6, Config.series.length + 1):
        collect_event_data(_race_number)

    for _race_number in range(1, Config.series.length + 1):
        create_race_leaderboard(_race_number)

    create_series_leaderboard()
    create_iso3166_1_leaderboard()

    generate_all_races_html()
    generate_league_table_html()