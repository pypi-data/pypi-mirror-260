import logging

from typing import Optional
from typing import Union
from typing import List
from typing import Callable
from typing import Dict

from .utils import convert_length
from .utils import convert_publication_date
from .utils import convert_number
from .utils import get_item_type

from .endpoints import Endpoint
from .endpoints import BrowseEndpoint
from .endpoints import WatchEndpoint
from .endpoints import UrlEndpoint
from .endpoints import SearchEndpoint

from .containers import CardShelf
from .containers import Shelf
from .containers import Container

from .exceptions import EndpointNotFound
from .exceptions import ITDEError
from .exceptions import UnregisteredItemType
from .exceptions import KeyNotFound
from .exceptions import UnexpectedState

from .items import Item
from .items import AlbumItem
from .items import VideoItem
from .items import ArtistItem
from .items import PlaylistItem
from .items import SongItem
from .items import SingleItem
from .items import EPItem
from .items import PodcastItem
from .items import ProfileItem
from .items import EpisodeItem

from .ytypes import ContinuationStrucType
from .ytypes import ItemStructType
from .ytypes import ShelfStructType
from .ytypes import ResultStructType
from .ytypes import EndpointType
from .ytypes import ShelfType
from .ytypes import ItemType


log = logging.getLogger(__name__)


def handle(function: Callable) -> Callable:
    def inner_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except (KeyError, IndexError, TypeError, ValueError, ITDEError) as error:

            log.error(
                "An error occured during the data extraction process. "
                "Please open an issue at https://github.com/g3nsy/itde/issues"
            )

            raise ITDEError(
                "An error occured during the data extraction process. "
            ) from error

    return inner_function


@handle
def extract(data: Dict) -> Container:
    header = _extract_item(data["header"]) if "header" in data else None

    data_contents = _extract_contents(data)

    container = Container(header=header, contents=None)

    if data_contents is None:
        return container

    contents: List[Shelf] = []

    for entry in data_contents:
        shelf = _extract_shelf(entry)
        if shelf is not None:
            contents.append(shelf)

    container.contents = contents
    return container


def _extract_contents(data: Dict) -> Optional[Union[Dict, List]]:
    if ContinuationStrucType.CONTINUATION.value in data:
        key = ContinuationStrucType.CONTINUATION.value

        if ContinuationStrucType.SECTION_LIST.value in data[key]:
            contents = data[key][ContinuationStrucType.SECTION_LIST.value]["contents"]

        elif ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value in data[key]:
            contents = [
                {
                    ShelfStructType.MUSIC_SHELF.value: data[key][
                        ContinuationStrucType.MUSIC_PLAYLIST_SHELF.value
                    ]
                }
            ]

        elif ContinuationStrucType.MUSIC_SHELF.value in data[key]:
            contents = [
                {
                    ShelfStructType.MUSIC_SHELF.value: data[key][
                        ContinuationStrucType.MUSIC_SHELF.value
                    ]
                }
            ]

        else:
            raise UnexpectedState

    elif ResultStructType.TWO_COLUMN_BROWSE_RESULT.value in data["contents"]:
        contents = data["contents"][ResultStructType.TWO_COLUMN_BROWSE_RESULT.value][
            "secondaryContents"
        ]["sectionListRenderer"]["contents"]

    elif ResultStructType.SINGLE_COLUMN_BROWSE_RESULTS.value in data["contents"]:
        tmp = data["contents"]["singleColumnBrowseResultsRenderer"]["tabs"][0][
            "tabRenderer"
        ]["content"]["sectionListRenderer"]

        if ShelfStructType.GRID.value in tmp["contents"][0]:
            contents = tmp["contents"]

        elif ShelfStructType.MUSIC_PLAYLIST_SHELF.value in tmp["contents"][0]:
            contents = tmp["contents"][0]["musicPlaylistShelfRenderer"]["contents"]

        elif ShelfStructType.MUSIC_SHELF.value in tmp["contents"][0]:
            contents = tmp["contents"]
        else:
            raise UnexpectedState

    elif ResultStructType.TABBED_SEARCH_RESULTS.value in data["contents"]:
        contents = data["contents"]["tabbedSearchResultsRenderer"]["tabs"][0][
            "tabRenderer"
        ]["content"]["sectionListRenderer"]["contents"]

    elif (
        ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value in data["contents"]
    ):
        contents = [
            data["contents"][
                ResultStructType.SINGLE_COLUMN_MUSIC_WATCH_NEXT_RESULT.value
            ]["tabbedRenderer"]["watchNextTabbedResultsRenderer"]["tabs"][0][
                "tabRenderer"
            ][
                "content"
            ][
                "musicQueueRenderer"
            ][
                "content"
            ]
        ]

    else:
        raise KeyNotFound(data["contents"].keys())

    return contents


def _extract_shelf(entry: Dict) -> Optional[Shelf]:
    if ShelfStructType.MUSIC_SHELF.value in entry:
        key = ShelfStructType.MUSIC_SHELF.value
        try:
            type = ShelfType(entry[key]["title"]["runs"][0]["text"])
            endpoint = _extract_endpoint(data=entry[key]["bottomEndpoint"])
        except (KeyError, TypeError):
            type = None
            endpoint = None
        entry_contents = entry[key]["contents"]
        try:
            continuation = entry[key]["continuations"][0]["nextContinuationData"][
                "continuation"
            ]
        except (IndexError, KeyError):
            continuation = None
        shelf = Shelf(
            type=type,
            endpoint=endpoint,
            continuation=continuation,
        )

    elif ShelfStructType.MUSIC_CAROUSEL_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CAROUSEL_SHELF.value
        entry_contents = entry[key]["contents"]
        type = ShelfType(
            entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"]["title"][
                "runs"
            ][0]["text"]
        )
        try:
            endpoint = _extract_endpoint(
                data=entry[key]["header"]["musicCarouselShelfBasicHeaderRenderer"][
                    "title"
                ]["runs"][0]["navigationEndpoint"]
            )
        except KeyError:
            endpoint = None
        shelf = Shelf(type=type, endpoint=endpoint, continuation=None)

    elif ShelfStructType.MUSIC_CARD_SHELF.value in entry:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        entry_contents = entry[key].get("contents", [])
        item = _extract_item(entry)
        if item:
            shelf = CardShelf(item=item)
        else:
            raise UnexpectedState(f"Unexpected {key} state.")

    elif ShelfStructType.PLAYLIST_PANEL.value in entry:
        key = ShelfStructType.PLAYLIST_PANEL.value
        name = entry[key].get("title", None)
        try:
            type = ShelfType(name)
        except (TypeError, ValueError):
            type = None
        entry_contents = entry[key]["contents"]
        shelf = Shelf(type=type, name=name, endpoint=None, continuation=None)  # TODO

    elif ShelfStructType.GRID.value in entry:
        key = ShelfStructType.GRID.value
        shelf = Shelf()
        entry_contents = entry[key]["items"]

    elif (ShelfStructType.ITEM_SECTION.value in entry) | (
        ShelfStructType.MUSIC_DESCRIPTION_SHELF.value in entry
    ):
        return None

    else:
        raise KeyNotFound(entry.keys())

    item_type = get_item_type(shelf.type) if shelf.type else None
    for entry_item in entry_contents:
        item = _extract_item(entry_item, item_type)
        if item:
            shelf.append(item)

    return shelf


def _extract_item(entry_item: Dict, type: Optional[ItemType] = None) -> Optional[Item]:
    if ShelfStructType.MUSIC_CARD_SHELF.value in entry_item:
        key = ShelfStructType.MUSIC_CARD_SHELF.value
        type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
        name = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(
            entry_item[key]["title"]["runs"][0]["navigationEndpoint"]
        )
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"
        ]["thumbnails"][-1]["url"]

        match type:
            case ItemType.ALBUM:
                item = AlbumItem(
                    # artist_items in entry[key]['subtitle'][1:]
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                )

            case ItemType.ARTIST:
                subscribers = convert_number(
                    entry_item[key]["subtitle"]["runs"][-1]["text"]
                )
                item = ArtistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )

            case ItemType.VIDEO:
                # artist_items in entry_item[key]['subtitle']['runs'][2:-3]
                views = convert_number(entry_item[key]["subtitle"]["runs"][-3]["text"])
                length = convert_length(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = VideoItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    views=views,
                    length=length,
                )

            case ItemType.EP:
                # artist_items in entry[key]['subtitle'][2:]
                item = EPItem(  # type: ignore
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url
                )

            case ItemType.SONG:
                length = convert_length(entry_item[key]["subtitle"]["runs"][-1]["text"])
                album_item = AlbumItem(
                    name=entry_item[key]["subtitle"]["runs"][-3]["text"],
                    endpoint=_extract_endpoint(
                        entry_item[key]["subtitle"]["runs"][-3]["navigationEndpoint"]
                    ),
                )
                item = SongItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    reproduction=None,
                    album_item=album_item,
                )

            case ItemType.EPISODE:
                # TODO artist_items in entry[key][subtitle][runs][4:]
                publication_date = convert_publication_date(
                    string=entry_item[key]["subtitle"]["runs"][2]
                )
                item = EpisodeItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    publication_date=publication_date,
                    length=None,
                )

            case _:
                raise UnregisteredItemType(type)

    elif ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_RESPONSIVE_LIST_ITEM.value
        try:
            thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
                "thumbnail"
            ]["thumbnails"][-1]["url"]
        except KeyError:
            thumbnail_url = None
        name = entry_item[key]["flexColumns"][0][
            "musicResponsiveListItemFlexColumnRenderer"
        ]["text"]["runs"][0]["text"]
        if type is None:
            try:
                type = ItemType(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][0]["text"]
                )
            except (KeyError, ValueError):
                # It appears that 'Song' items
                # do not have 'Song' in the subtitle
                type = ItemType.SONG

        match type:

            case ItemType.ARTIST:
                try:
                    subscribers = convert_number(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["text"]
                    )
                except UnexpectedState:
                    subscribers = None
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = ArtistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )

            case ItemType.ALBUM:
                release_year = int(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][-1]["text"]
                )
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = AlbumItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )

            case ItemType.VIDEO:
                length = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"
                ]["text"]["runs"][-1]["text"]
                views = convert_number(
                    entry_item[key]["flexColumns"][1][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][-3]["text"]
                )
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][-1]["navigationEndpoint"]
                )
                item = VideoItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    views=views,
                )

            case ItemType.PLAYLIST:
                try:
                    tracks_num = int(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    tracks_num = None

                try:
                    views = convert_number(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["text"]
                    )
                except (KeyError, IndexError, ValueError):
                    views = None  # type: ignore

                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])

                item = PlaylistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    views=views,
                )

            case ItemType.SINGLE:
                release_year = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"
                ]["text"]["runs"][-1]["text"]
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = SingleItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=int(release_year),
                )

            case ItemType.SONG:

                try:
                    length = convert_length(
                        entry_item[key]["flexColumns"][1][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["text"]
                    )
                except (UnexpectedState, KeyError):
                    length = None

                try:
                    reproduction = convert_number(
                        entry_item[key]["flexColumns"][-1][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["text"]
                    )
                except (UnexpectedState, KeyError):
                    try:
                        reproduction = convert_number(
                            entry_item[key]["flexColumns"][-2][
                                "musicResponsiveListItemFlexColumnRenderer"
                            ]["text"]["runs"][-1]["text"]
                        )
                    except (UnexpectedState, KeyError):
                        reproduction = None

                try:
                    endpoint = _extract_endpoint(
                        data=entry_item[key]["flexColumns"][0][
                            "musicResponsiveListItemFlexColumnRenderer"
                        ]["text"]["runs"][-1]["navigationEndpoint"]
                    )
                except KeyError:
                    endpoint = None

                item = SongItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=length,
                    reproductions=reproduction,
                    album_item=None,
                )

            case ItemType.EPISODE:
                endpoint = _extract_endpoint(
                    data=entry_item[key]["flexColumns"][0][
                        "musicResponsiveListItemFlexColumnRenderer"
                    ]["text"]["runs"][-1]["navigationEndpoint"]
                )
                item = EpisodeItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    publication_date=None,
                )

            case ItemType.PODCAST:
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = PodcastItem(  # type: ignore
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url
                )

            case ItemType.PROFILE:
                item_handle = entry_item[key]["flexColumns"][1][
                    "musicResponsiveListItemFlexColumnRenderer"
                ]["text"]["runs"][-1]["text"]
                item = ProfileItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    handle=item_handle,
                )

            case ItemType.EP:
                endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])
                item = EPItem(  # type: ignore
                    name=name, endpoint=endpoint, thumbnail_url=thumbnail_url
                )

            case _:
                raise UnregisteredItemType(type)

    elif ItemStructType.MUSIC_TWO_ROW_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_TWO_ROW_ITEM.value
        thumbnail_url = entry_item[key]["thumbnailRenderer"]["musicThumbnailRenderer"][
            "thumbnail"
        ]["thumbnails"][-1]["url"]
        name = entry_item[key]["title"]["runs"][0]["text"]
        endpoint = _extract_endpoint(data=entry_item[key]["navigationEndpoint"])

        if type is None:
            try:
                type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
            except ValueError:
                type = ItemType.SINGLE

        match type:

            case ItemType.ARTIST:
                subscribers = convert_number(
                    entry_item[key]["subtitle"]["runs"][0]["text"]
                )
                item = ArtistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    subscribers=subscribers,
                )

            case ItemType.ALBUM:
                try:
                    release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                except ValueError:
                    release_year = None
                item = AlbumItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )

            case ItemType.EP:
                release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                # no associated artists
                item = EPItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    artist_items=None,
                    release_year=release_year,
                )

            case ItemType.VIDEO:
                views = convert_number(entry_item[key]["subtitle"]["runs"][-1]["text"])
                item = VideoItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=views,
                )

            case ItemType.PLAYLIST:
                item = PlaylistItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    views=None,
                )

            case ItemType.SINGLE:
                try:
                    release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
                except ValueError:
                    release_year = None
                item = SingleItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    release_year=release_year,
                )

            case ItemType.SONG:
                item = SongItem(  # type: ignore
                    name=name,
                    endpoint=endpoint,
                    thumbnail_url=thumbnail_url,
                    length=None,
                    reproductions=None,
                    album_item=None,
                )

            case ItemType.EPISODE | ItemType.PODCAST | ItemType.PROFILE:
                raise UnexpectedState(type)

            case _:
                raise UnregisteredItemType(type)

    elif ItemStructType.PLAYLIST_PANEL_VIDEO.value in entry_item:
        key = ItemStructType.PLAYLIST_PANEL_VIDEO.value
        name = entry_item[key]["title"]["runs"][-1]["text"]
        endpoint = _extract_endpoint(entry_item[key]["navigationEndpoint"])
        length = convert_length(entry_item[key]["lengthText"]["runs"][-1]["text"])
        tmp = entry_item[key]["thumbnail"]["thumbnails"][-1]
        thumbnail_url = entry_item[key]["thumbnail"]["thumbnails"][-1]["url"]
        width, height = tmp["width"], tmp["height"]

        # In this case it is impossible to determine the type of the items
        # It seems that the songs have a cover whose size ratio is 1,
        # while the remaining items do not
        if width / height == 1:
            item = SongItem(  # type: ignore
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                album_item=None,
            )

        # Podcasts, episodes and videos are collected here.
        else:
            try:
                views = convert_number(
                    entry_item[key]["longBylineText"]["runs"][-3]["text"]
                )
            except (KeyError, IndexError):
                views = None

            item = VideoItem(  # type: ignore
                name=name,
                endpoint=endpoint,
                thumbnail_url=thumbnail_url,
                length=length,
                views=views,
            )

    elif ItemStructType.MUSIC_IMMERSIVE_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_IMMERSIVE_HEADER.value
        try:
            description = entry_item[key]["description"]["runs"][0]["text"]
        except KeyError:
            description = None
        item = ArtistItem(  # type: ignore
            name=entry_item[key]["title"]["runs"][0]["text"],
            description=description,
            thumbnail_url=entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
                "thumbnail"
            ]["thumbnails"][-1]["url"],
            subscribers=entry_item[key]["subscriptionButton"][
                "subscribeButtonRenderer"
            ]["subscriberCountText"]["runs"][0]["text"],
            endpoint=None,
        )

    elif ItemStructType.MUSIC_DETAIL_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_DETAIL_HEADER.value
        type = ItemType(entry_item[key]["subtitle"]["runs"][0]["text"])
        name = entry_item[key]["title"]["runs"][0]["text"]
        thumbnail_url = entry_item[key]["thumbnail"]["croppedSquareThumbnailRenderer"][
            "thumbnail"
        ]["thumbnails"][-1]["url"]
        release_year = int(entry_item[key]["subtitle"]["runs"][-1]["text"])
        if type is ItemType.PLAYLIST:
            tracks_num = entry_item[key]["secondSubtitle"]["runs"][2]["text"]
        else:
            tracks_num = entry_item[key]["secondSubtitle"]["runs"][0]["text"]

        # TODO artist_items
        match type:
            case ItemType.ALBUM:
                item = AlbumItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )

            case ItemType.EP:
                item = EPItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )

            case ItemType.SINGLE:
                item = SingleItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                )

            case ItemType.PLAYLIST:
                views = convert_number(
                    entry_item[key]["secondSubtitle"]["runs"][0]["text"]
                )
                item = PlaylistItem(  # type: ignore
                    name=name,
                    endpoint=None,
                    thumbnail_url=thumbnail_url,
                    tracks_num=tracks_num,
                    release_year=release_year,
                    views=views,
                )

            case _:
                raise UnexpectedState(type)

    elif ItemStructType.MUSIC_VISUAL_HEADER.value in entry_item:
        key = ItemStructType.MUSIC_VISUAL_HEADER.value
        name = entry_item[key]["title"]["runs"][-1]["text"]
        # TODO foreground thumbnail !?
        thumbnail_url = entry_item[key]["thumbnail"][
            "musicThumbnailRenderer"]["thumbnail"][
            "thumbnails"][-1]["url"]
        item = Item(  # type: ignore
            name=name, 
            thumbnail_url=thumbnail_url,
        )

    elif ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value in entry_item:
        key = ItemStructType.MUSIC_MULTI_ROW_LIST_ITEM.value
        name = entry_item[key]["title"]["runs"][0]["text"]
        thumbnail_url = entry_item[key]["thumbnail"]["musicThumbnailRenderer"][
            "thumbnail"
        ]["thumbnails"][-1]["url"]
        endpoint = _extract_endpoint(
            entry_item[key]["title"]["runs"][0]["navigationEndpoint"]
        )
        item = Item(  # type: ignore
            name=name, thumbnail_url=thumbnail_url, endpoint=endpoint
        )

    elif (
        (ItemStructType.AUTOMIX_PREVIEW_VIDEO.value in entry_item)
        | (ItemStructType.PLAYLIST_EXPANDABLE_MESSAGE.value in entry_item)
        | (ItemStructType.MESSAGE.value in entry_item)
    ):
        return None

    else:
        raise KeyNotFound(f"Content: {entry_item.keys()}")

    return item


def _extract_endpoint(data: Dict) -> Endpoint:
    if EndpointType.BROWSE_ENDPOINT.value in data:
        endpoint_data = data["browseEndpoint"]
        browse_id = endpoint_data["browseId"]
        endpoint = BrowseEndpoint(
            browse_id=browse_id, params=endpoint_data.get("params", None)
        )

    elif EndpointType.WATCH_ENDPOINT.value in data:
        endpoint_data = data["watchEndpoint"]
        video_id = endpoint_data["videoId"]
        endpoint = WatchEndpoint(  # type: ignore
            video_id=video_id,
            playlist_id=endpoint_data.get("playlist_id", None),
            params=endpoint_data.get("params", None),
        )

    elif EndpointType.SEARCH_ENDPOINT.value in data:
        endpoint_data = data["searchEndpoint"]
        query = endpoint_data["query"]
        endpoint = SearchEndpoint(  # type: ignore
            query=query, params=endpoint_data.get("params", None)
        )

    elif EndpointType.URL_ENDPOINT in data:
        endpoint_data = data["urlEndpoint"]
        url = endpoint_data["url"]
        endpoint = UrlEndpoint(  # type: ignore
            url=url, params=endpoint_data.get("params", None)
        )

    else:
        raise EndpointNotFound(f"Endpoint not found in: {data}")

    return endpoint
