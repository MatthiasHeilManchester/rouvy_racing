from enum import IntEnum, Enum
import enum
"""
A place to stor all the enums for the project
"""


@enum.unique
class IsoDow(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    ALL = 8

    def __format__(self, spec):
        return f'{self._name_.capitalize()}'


@enum.unique
class RaceMonth(IntEnum):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12
    ALL = 13

    def __format__(self, spec):
        return f'{self._name_.capitalize()}'


@enum.unique
class HTTPMethod(Enum):  # This exists in Python 3.11+
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


@enum.unique
class Files(Enum):
    JSON_USER_DATA = "user_data.json"
    JSON_ROUTE = "route.json"
    JSON_RACES = "races.json"


@enum.unique
class RouvyEventType(Enum):
    RACE = 'RACE'
    GROUP_RIDE = 'GROUP_RIDE'


@enum.unique
class RouvyEventOrganizer(Enum):
    ALL = 'all'
    OFFICIAL = 'official'
    UNOFFICIAL = 'unofficial'


@enum.unique
class RouvyEventStatus(Enum):
    FINISHED = 'FINISHED'
    UNFINISHED = 'UNFINISHED'
