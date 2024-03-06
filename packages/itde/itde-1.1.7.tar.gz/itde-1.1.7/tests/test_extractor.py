import logging
import time
import os
import sys
import json
from rich import traceback
from rich.console import Console
from datetime import datetime
from innertube import InnerTube  # type: ignore

from typing import Optional
from typing import Callable
from typing import Dict

# ITDE imports
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
ITDE_DIR = os.path.dirname(TEST_DIR)
sys.path.append(ITDE_DIR)
from itde import Container  # noqa
from itde import extractor  # noqa
from itde import Item  # noqa

# log setup
traceback.install()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console = Console()

SAVE_DATA = True
INNERTUBE_CLIENT = InnerTube("WEB_REMIX")
INNERTUBE_DATA_PATH = os.path.join(TEST_DIR, "innertube")
TESTS_DATA_PATH = os.path.join(TEST_DIR, "test-data.json")
with open(TESTS_DATA_PATH, mode="r", encoding="utf-8") as file:
    TESTS_DATA = json.load(file)


def rich_traceback(func: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException:
            console.print_exception()

    return inner_function


@rich_traceback
def test_function(
    test_type: str,
    save_data: bool = SAVE_DATA,
) -> None:
    console.rule(f"[bold green] {test_type}")
    for entry in TESTS_DATA["tests"][f"{test_type}"]:
        console.rule(f"[bold white] {entry['test_name']}")
        match test_type:
            case "search":
                data = INNERTUBE_CLIENT.search(
                    query=entry["query"],
                    params=entry["params"],
                    continuation=entry["continuation"],
                )
            case "browse":
                data = INNERTUBE_CLIENT.browse(
                    browse_id=entry["browse_id"],
                    params=entry["params"],
                    continuation=entry["continuation"],
                )
            case "next":
                data = INNERTUBE_CLIENT.next(
                    video_id=entry["video_id"],
                    playlist_id=entry["playlist_id"],
                    params=entry["params"],
                    index=entry["index"],
                    continuation=entry["continuation"],
                )
            case _:
                raise RuntimeError(f"Invalid test type: {test_type}")

        if save_data:
            save(prefix=f'{entry["test_name"]}', data=data)

        extracted_data = _extract(data)

        console.print(extracted_data)

        if extracted_data:
            if extracted_data.header:
                console.print(extracted_data.header)

            if extracted_data.contents:
                for content in extracted_data.contents:
                    for shelf in content:
                        time.sleep(0.08)
                        console.print(str(shelf)[:170])


@rich_traceback
def _extract(data: Dict) -> Optional[Container]:
    return extractor.extract(data=data)


def save(prefix: str, data: Dict) -> None:
    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S_%f")
    filename = f"{prefix}_{now}.json"
    path = os.path.join(INNERTUBE_DATA_PATH, filename)
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def main() -> None:
    test_function("search")
    test_function("next")
    test_function("browse")


if __name__ == "__main__":
    main()
