from typing import List
from typing import Optional
from .items import Item
from .ytypes import ShelfType
from .endpoints import Endpoint


class Shelf(List[Item]):
    def __init__(
        self,
        type: Optional[ShelfType] = None,
        name: Optional[str] = None,
        endpoint: Optional[Endpoint] = None,
        continuation: Optional[str] = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.type = type
        self.name = name
        self.endpoint = endpoint
        self.continuation = continuation

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Shelf):
            return (
                self.type == __value.type
                and self.name == __value.name
                and self.endpoint == __value.endpoint
                and self.continuation == __value.continuation
                and super().__eq__(__value)
            )
        else:
            return False

    def __repr__(self) -> str:
        return (
            "Shelf{"
            f"type={self.type}, "
            f"endpoint={self.endpoint}, "
            f"continuation={self.continuation}, "
            f"items={super().__repr__()}"
            "}"
        )


class CardShelf(Shelf):
    def __init__(self, item: Item) -> None:
        super().__init__(type=ShelfType.TOP_RESULT)
        self.item = item

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, CardShelf):
            return (
                self.type == __value.type
                and self.name == __value.name
                and self.endpoint == __value.endpoint
                and self.continuation == __value.continuation
                and self.item == __value.item
                and super().__eq__(__value)
            )
        else:
            return False

    def __repr__(self) -> str:
        return (
            "CardShelf{"
            f"item={self.item}, "
            f"type={self.type}, "
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"items={super(list, self).__repr__()}"
        )


class Container:
    def __init__(self, header: Optional[Item], contents: Optional[List[Shelf]]) -> None:
        self.header = header
        self.contents = contents

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Container):
            return self.header == __value.header and self.contents == __value.contents
        else:
            return False

    def __repr__(self) -> str:
        return "Container{" f"header={self.header}, " f"contents={self.contents}" "}"
