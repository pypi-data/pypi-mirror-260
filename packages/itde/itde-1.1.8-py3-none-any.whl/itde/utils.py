import re
from typing import Callable
from typing import Optional
from datetime import time
from datetime import date
from .ytypes import ShelfType
from .ytypes import ItemType
from .exceptions import UnregisteredShelfType
from .exceptions import UnexpectedState


def handle(function: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (AttributeError, ValueError, IndexError, TypeError) as error:
            raise UnexpectedState(
                f"Unexpected state detected: {error.args[0]}"
            ) from error

    return inner_function


@handle
def convert_number(string: str) -> int:

    match = re.search(r"(\d+\.\d+|\d+)([BMK])?", string)

    result = match.group() if match else ""
    last_char = result[-1]

    if last_char.isupper():
        number = float(result[:-1])
        match last_char:
            case "B":
                factor = 1000000000
            case "M":
                factor = 1000000
            case "K":
                factor = 1000
            case _:
                raise ValueError(f"Unexpected character: {last_char}")
        return int(number * factor)
    else:
        return int(result)


@handle
def convert_length(string: str) -> time:
    time_list = [int(x) for x in string.split(":")]
    match len(time_list):
        case 3:
            return time(hour=time_list[0], minute=time_list[1], second=time_list[2])
        case 2:
            return time(minute=time_list[0], second=time_list[1])
        case _:
            raise ValueError(f"Unexpected time format: {string}")


@handle
def convert_publication_date(string: str) -> date:
    month, day, year = string.split()
    return date(month=convert_month(month), day=int(day[:-1]), year=int(year))


@handle
def convert_month(month: str) -> int:
    match month.lower():
        case "jan":
            return 1
        case "feb":
            return 2
        case "mar":
            return 3
        case "apr":
            return 4
        case "may":
            return 5
        case "jun":
            return 6
        case "jul":
            return 7
        case "aug":
            return 8
        case "sep":
            return 9
        case "oct":
            return 10
        case "nov":
            return 11
        case "dec":
            return 12
        case _:
            raise ValueError("Unexpected month: {month}")


def get_item_type(shelf_type: ShelfType) -> Optional[ItemType]:
    match shelf_type:

        case ShelfType.SONG | ShelfType.SONGS:
            return ItemType.SONG

        case ShelfType.SINGLES:
            return ItemType.SINGLE

        case ShelfType.VIDEO | ShelfType.VIDEOS:
            return ItemType.VIDEO

        case (
            ShelfType.FEATURED_PLAYLIST
            | ShelfType.COMMUNITY_PLAYLIST
            | ShelfType.PLAYLIST
            | ShelfType.FEATURED_ON
        ):
            return ItemType.PLAYLIST

        case ShelfType.ALBUM | ShelfType.ALBUMS:
            return ItemType.ALBUM

        case ShelfType.ARTIST | ShelfType.ARTISTS | ShelfType.FANS_MIGHT_ALSO_LIKE:
            return ItemType.ARTIST

        case ShelfType.EPISODE | ShelfType.EPISODES:
            return ItemType.EPISODE

        case ShelfType.PROFILES:
            return ItemType.PROFILE

        case ShelfType.PODCASTS:
            return ItemType.PODCAST

        case ShelfType.TOP_RESULT | ShelfType.OTHER_VERSIONS:
            return None

        case _:
            raise UnregisteredShelfType(shelf_type)
