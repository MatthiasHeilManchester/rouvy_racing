import sh
import json
import requests
from time import sleep
from pathlib import Path
from config import Config, Constants
from typing import Optional
from http import HTTPStatus
from enums import HTTPMethod, RouvyEventType
from datetime import datetime, timezone
from requests import Session, Response
__session: Optional[requests.Session] = None
__last_request_time: datetime = datetime.now(timezone.utc)
"""
Common things
"""


def nice_request(url: str, method: HTTPMethod = HTTPMethod.GET, payload=None) -> Response:
    """
    Do a nice request, use a rate limit and allow for retries
    :param url: The url to request
    :param method: The HTTP method to use
    :param payload: The payload to send to the url
    :return: A Response object
    """
    okay_enough:list = [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT]
    global __last_request_time
    sleep_time: float = max(0.0, Constants.REQUEST_RATE_LIMIT -
                            (datetime.now(timezone.utc) - __last_request_time).total_seconds())
    sleep(sleep_time)  # slow down if we need to
    response: Response = Response()
    status_code = HTTPStatus.IM_A_TEAPOT  # Python 3.9
    for retry in range(0, Constants.REQUEST_RETRY_LIMIT + 1):
        if retry > 0:
            print(f'[?] Request failed with status {status_code} {response.reason} attempting retry {retry}')
            print(f'    Request body {response.request.body}')
            print(f'    Response raw {response.text}')
            sleep(Constants.REQUEST_RETRY_DELAY * retry)
        session: Session = get_authenticated_session()
        if method == HTTPMethod.GET:
            response: Response = session.get(url=url)
        elif method == HTTPMethod.POST:
            response: Response = session.post(url=url, data=payload)
        else:
            raise NotImplementedError(f'Method {method} not implemented')
        __last_request_time = datetime.now(timezone.utc)
        status_code: int = response.status_code
        if status_code in okay_enough:
            break

    attempt:dict = {1:'2nd', 2:'3rd'} # Yes this will sound dumb on the "21th" attempt, but let's not try that many.
    if retry > 0 and status_code in okay_enough:
        print(f"[*] That was lucky, it worked on the {attempt.get(retry, str(retry+1) + 'th')} attempt")

    if status_code not in okay_enough:
        print(f'[X] Request failed with status {status_code} {response.reason}')
        print(f'    Request body {response.request.body}')
        print(f'    Response raw {response.text}')
        exit(1)

    return response


def get_authenticated_session() -> Session:
    """
    Logs into rouvy and returns an authenticated session we can use for requests
    :return: An authenticated Session
    """
    # Reuse the session we have or create a new one
    global __session
    if __session is not None:
        return __session

    status_code = HTTPStatus.IM_A_TEAPOT
    for retry in range(0, Constants.REQUEST_RETRY_LIMIT + 1):
        if retry > 0:
            print(f'[?] Login failed with status {status_code} attempting retry {retry}')
            sleep(Constants.REQUEST_RETRY_DELAY * retry)
        session = Session()
        payload = {'email': Config.rouvy.email,
                   'password': Config.rouvy.password}
        try:
            response: Response = session.post("https://riders.rouvy.com/login", payload)
        except requests.exceptions.ConnectionError:
            print("[X] Connection error, no internet?")
            continue  # Let's give it another go
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            print("[*] Login Success")
            # Force our session to GMT / UTC
            session.cookies.set("CH-time-zone", "Greenwich", domain="riders.rouvy.com")
            __session = session  # let's keep the same sessions going...
            return session

        print(f"[X] Login Fail :( error: {response.status_code}")
        exit(1)


def json_date_to_datetime(json_date: str) -> datetime:
    """
    Converts a JSON date string to a datetime object.
    :param json_date: JSON date string.
    :return: datetime object.
    """
    dt: datetime = datetime.strptime(json_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt


def backup_series() -> int:
    """
    Backup series with tar lzma (about 3 times smaller than gz)
    zero exception handling, they will bubble up
    :return: The tar return code
    """
    ts: str = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    backup_path = Path(Config.series.data_path, 'Backup')
    backup_path.mkdir(exist_ok=True)
    series_folder: str = Config.series.series_path.name
    backup_name: str = Path(backup_path, f'{series_folder}_{ts}.tar.gz').as_posix()
    series_path: str = Config.series.series_path.as_posix()
    result = sh.tar(('cvfz', backup_name, series_path), _return_cmd=True)
    return result.exit_code


def __get_remix_node_name(node: str, j: json) -> str:
    """
    Gets the node name
    :param node: node id string
    :param j: RemixJS Data
    :return: Node name
    """
    assert node.startswith('_'), f'NodeID does not start with _: {node}'
    node_id: int
    try:
        node_id = int(node[1:])
    except ValueError:
        assert False, f'NodeID not int: {node}'
    node_name: str = j[node_id]
    return node_name


def __parse_remix_node(node_id: int, remix_data: json) -> dict:
    """
    Recursively parse RemixJS data
    :param node_id: Starting node_id
    :param remix_data: RemixJS data
    :return: Dictionary
    """
    # Looks like -5 is null
    parsed_dict: dict = dict()
    if node_id == -5:
        print(node_id)
        parsed_dict = None
        return parsed_dict
    # Know idea if any other special values
    if node_id < 0:
        print(f"*** Negitave NodeID found: {node_id} please let me know ***")
        parsed_dict = {"Negative Node": node_id}
        return parsed_dict
    node_data = remix_data[node_id]
    assert type(node_data) is dict, f'NodeData not dict: {node_data}'
    for k, v in node_data.items():
        node_name = __get_remix_node_name(k, remix_data)
        val = remix_data[v]
        # Expecting a:
        # * Dictionary to nest into, or
        # * List to iterate through, or
        # * A value
        if type(val) is dict:
            parsed_dict[node_name] = __parse_remix_node(v, remix_data) # v or val
        elif type(val) is list:
            for list_item in val:
                if list_item == 'P':
                    # P Node Found
                    # TODO: collect the next value in the list
                    # TODO: Do something with this, if required, they are the other lines in he RemixJS data
                    break  # For now, we just ignore them
                if type(list_item) is int:
                    node_list = parsed_dict.get(node_name, [])
                    node_data = remix_data[int(list_item)]
                    # Seen so far list of Dict, str, int
                    if type(node_data) is dict:
                        # recursively dig the dictionary
                        node_list.append(__parse_remix_node(int(list_item), remix_data))
                    elif type(node_data) in [int, str]:
                        node_list.append(node_data)
                    else:
                        assert False, f'NodeData not dict, int or list: {node_data}'
                    parsed_dict[node_name] = node_list
                else:
                    assert False, f"Some other value in list: '{list_item}'"
        else:
            parsed_dict[node_name] = val
    return parsed_dict


def remix_parse(data: str, debug: bool = False) -> dict:
    """
    A partial paser for RemixJS data
    Only looks at the first / root data stream
    Ignores PNodes (that's what I call them anyway)
    :param debug: Optional, set to True to print debug messages
    :param data: RemixJS data
    :return: A nice dictionary from RemixJS data
    """
    parts = data.split('\n')
    root: json = json.loads(parts[0])
    if debug:
        i = 0
        for x in root:
            print(f"{i}\t{x}")
            i += 1

    # Recursively parse the nodes in the RemixJS data
    d = __parse_remix_node(0, root)

    if debug:
        print(json.dumps(d, indent=2))

    return d


if __name__ == '__main__':
    pass
    #######################################################################
    # Some tests for future me
    # At some point Rouvy will likely kill off the old json api calls
    #######################################################################
    # route = "events_.$id" <- this is the wrong node for the leaderboard
    # url = f"https://riders.rouvy.com/events/041c2d52-1230-4f82-be89-fb6abdec970f/leaderboard.data"#?_routes=routes/_main.{route}"
    # result = nice_request(url=url)
    # remix_data = remix_parse(result.text, True)
    #
    # route = "events_.$id"
    # url = f"https://riders.rouvy.com/events/20cefe5e-ddf6-4729-a16e-cc9c03011f82.data?_routes=routes/_main.{route}"
    # result = nice_request(url=url)
    # remix_data = remix_parse(result.text, True)

    # route = "challenges.status.$status"
    # for x in ['']:  # ['open', 'actual', 'planned', 'finished']:
    #     url = f"https://riders.rouvy.com/challenges/status/{x}.data?_routes=routes/_main.{route}"
    #     result = nice_request(url=url)
    #     remix_data = remix_parse(result.text, True)

    # route = "friends_.search"
    # url = f"https://riders.rouvy.com/friends/search.data?query=spacech&_routes=routes/_main.{route}"
    # result = nice_request(url=url)
    # remix_data = remix_parse(result.text, True)
    #
    # route = "new-route.$id"
    # url = f"https://riders.rouvy.com/new-route/96635.data?_routes=routes/_main.{route}"
    # result = nice_request(url=url)
    # remix_data = remix_parse(result.text, True)
    #
    # race_title = 'rvy_racing'
    # event_type = RouvyEventType.RACE
    # date_from = "2024-10-01"
    # date_to = "2024-11-01"
    # route = "events.search"
    # url = (f"https://riders.rouvy.com/events/search.data?searchQuery={race_title}&"
    #        f"smartTrainersOnly=true&"
    #        f"type={event_type.value}&"
    #        f"dateRange=custom&"
    #        f"dateFrom={date_from}&"
    #        f"dateTo={date_to}&"
    #        f"_routes=routes/_main.{route}")
    # result = nice_request(url=url)
    # remix_data = remix_parse(result.text, True)
