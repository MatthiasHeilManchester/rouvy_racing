import bs4
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pathlib import Path
from config import Config
from enums import Files
"""
Quick dirty hack to generate leaderboard.json files for the Events lost in the Rouvy site update
Paths are hard coded, you may need to check / change them
"""


# Maps the HTML column names to nice keys, consistent with the project
RESULT_NAME_MAP = {'Rank': 'aggPosition',
                   'Rouvy username': 'userName',
                   'First name': 'rvy_fname',
                   'Surname': 'rvy_sname',
                   'YOB': 'rvy_yob',
                   'Gender': 'rvy_gender',
                   'Finish time': 'time',
                   'Points': 'rvy_points'}


def parse_result_table(race: str, rt: bs4.BeautifulSoup) -> list:
    user_file = Path(Config.series.series_path, Files.JSON_USER_DATA.value)
    users: dict = json.load(user_file.open(mode='r', encoding='utf-8'))

    thead = rt.find("tr")
    # Get the table column names
    # Expect '#', 'Rider' 'Category', 'Age', 'Team', 'Time', 'Gap', 'Power', 'Avg Speed'
    # Should better check this, if any are missing or the name is different stuf will fail, YOLO
    # Col names are mapped to nice names, if stuff changes the map is all that will need to be updated
    # jinja templates will stay the same
    col_names = list()
    for val in thead.find_all("th"):
        rouvy_col_name = ' '.join(val.stripped_strings)
        nice_col_name = RESULT_NAME_MAP.get(rouvy_col_name, rouvy_col_name)
        col_names.append(nice_col_name)

    result_data = list()
    row_num = 0
    for result_row in rt.find_all("tr"):
        row_num += 1
        if row_num == 1:
            continue
        col = 0
        html_data: dict = dict()
        for val in result_row.find_all("td"):
            html_data[col_names[col]] = ' '.join(val.stripped_strings)
            col += 1

        user_data = users[html_data['userName']]
        if user_data['rouvy'].get('error', 'OK') != 'OK':
            if html_data['time'] != 'DNR':
                print(f"Issue with {users[html_data['userName']]}")
                print(html_data)
                continue
        time_sec = 0
        time = html_data['time']
        status: str = 'finished'
        if not time[0].isdigit():
            status = time
        else:
            dt = datetime.strptime(time, '%H:%M:%S.%f') - datetime(1900, 1, 1)
            time_sec = dt.total_seconds()
        row_data = dict(userName=user_data['rvy_rouvy_name'],
                        firebaseUID=user_data['rouvy'].get('firebaseUid', ''),
                        team="",
                        time=time,
                        timeSeconds=time_sec,
                        avatarUrl=user_data['rouvy'].get('avatar', ''),
                        avgWattKg="",
                        avgSpeedmps="",
                        countryCode=user_data['rouvy'].get('countryCode', 'XX'),
                        ageGroup="",
                        gender=user_data['rvy_gender'],
                        userSessionStatus=status,
                        aggPosition=int(html_data["aggPosition"]),
                        rvy_points=int(html_data["rvy_points"]),
                        rvy_username=user_data['rvy_username'],
                        rvy_rouvy_name=user_data['rvy_rouvy_name'],
                        rvy_fname=user_data["rvy_fname"],
                        rvy_sname=user_data["rvy_sname"],
                        rvy_strava_url=user_data['rvy_strava_url'],
                        rvy_yob=user_data["rvy_yob"],
                        rvy_gender=user_data["rvy_gender"],
                        rvy_allow=user_data["rvy_allow"])
        result_data.append({**row_data, **user_data})

    return result_data


def get_race_results(race: str):
    with open(f'../generated_html/rvy_racing/{race}/results.html', mode='r', encoding='UTF-8') as f:
        soup = BeautifulSoup(f, "html.parser")
    # Get the result_table, currently only one table on the page / it is the first table
    rt = soup.find("table")
    result_data = parse_result_table(race, rt)
    agg_file = f"../master_race_data/rvy_racing-2024-05/{race}/{Files.JSON_RACE_LEADERBOARD.value}"
    with open(agg_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # The lost events
    get_race_results('race00001')
    get_race_results('race00002')
    get_race_results('race00003')
    get_race_results('race00004')
    get_race_results('race00005')
