from typing import Optional
from .ytypes import EndpointType


class Endpoint:
    def __init__(
        self,
        params: Optional[str] = None,
        continuation: Optional[str] = None,
    ) -> None:
        self.params = params
        self.continuation = continuation
        self.type: Optional[EndpointType] = None

    def __repr__(self):
        return (
            "Endpoint{"
            f"type={self.type}, "
            f"params={self.params}, "
            f"continuation={self.continuation}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (
                self.type == __value.type and
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self):
        return hash((self.params, self.continuation, self.type))


class BrowseEndpoint(Endpoint):
    def __init__(self, browse_id: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.browse_id: str = browse_id
        self.type = EndpointType.BROWSE_ENDPOINT

    def __repr__(self):
        return super().__repr__()[:-1] + f", browse_id={self.browse_id}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BrowseEndpoint):
            return (
                self.type == __value.type and
                self.params == __value.params and
                self.browse_id == __value.browse_id and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self):
        return hash((self.params, self.continuation, self.type, self.browse_id))


class SearchEndpoint(Endpoint):
    def __init__(self, query: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.query: str = query
        self.type = EndpointType.SEARCH_ENDPOINT

    def __repr__(self):
        return super().__repr__()[:-1] + f", query={self.query}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, SearchEndpoint):
            return (
                self.type == __value.type and
                self.query == __value.query and
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self):
        return hash((self.params, self.continuation, self.type, self.query))


class WatchEndpoint(Endpoint):
    def __init__(
        self,
        video_id: str,
        playlist_id: Optional[str] = None,
        index: Optional[int] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.video_id = video_id
        self.index = index
        self.playlist_id = playlist_id
        self.type = EndpointType.WATCH_ENDPOINT

    def __repr__(self):
        return (
            super().__repr__()[:-1] + 
            f", video_id={self.video_id}"
            f", playlist_id={self.playlist_id}"
            f", index={self.index}"
            "}"
        )

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, WatchEndpoint):
            return (
                self.type == __value.type and
                self.index == __value.index and
                self.params == __value.params and
                self.video_id == __value.video_id and
                self.playlist_id == __value.playlist_id and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self):
        return hash((
            self.params, 
            self.continuation, 
            self.type, 
            self.video_id, 
            self.playlist_id, 
            self.index
        ))


class UrlEndpoint(Endpoint):
    def __init__(self, url: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.url: str = url
        self.type = EndpointType.URL_ENDPOINT

    def __repr__(self):
        return super().__repr__()[:-1] + f", url={self.url}" "}"

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, UrlEndpoint):
            return (
                self.url == __value.url and
                self.type == __value.type and
                self.params == __value.params and
                self.continuation == __value.continuation
            )
        else:
            return False

    def __hash__(self):
        return hash((self.params, self.continuation, self.type, self.url))

