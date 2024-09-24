import sh
import requests
from time import sleep
from pathlib import Path
from config import Config, Constants
from typing import Optional
from http import HTTPStatus
from enums import HTTPMethod
from datetime import datetime
from requests import Session, Response
__session: Optional[requests.Session] = None
__last_request_time: datetime = datetime.utcnow()
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
                            (datetime.utcnow() - __last_request_time).total_seconds())
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
        __last_request_time = datetime.utcnow()
        status_code: int = response.status_code
        if status_code in okay_enough:
            break

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


if __name__ == '__main__':
    pass
