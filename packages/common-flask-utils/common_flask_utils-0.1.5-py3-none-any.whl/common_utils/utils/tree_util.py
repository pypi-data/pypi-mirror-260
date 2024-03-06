from abc import ABC, abstractmethod
from typing import List


class T(ABC):
    @abstractmethod
    def keys(self) -> List[str]:
        pass


from typing import List, TypeVar

T = TypeVar("T")


def from_list(
    items: List[T],
    primary_key: str = "id",
    parent_key: str = "pid",
    children_key: str = "children",
) -> List[T]:
    """
    Converts a list of items into a tree-like structure based on the specified keys.

    Args:
        items (List[T]): The list of items to convert into a tree structure.
        primary_key (str, optional): The key representing the primary identifier of each item. Defaults to "id".
        parent_key (str, optional): The key representing the parent identifier of each item. Defaults to "pid".
        children_key (str, optional): The key representing the children of each item. Defaults to "children".

    Returns:
        List[T]: The list of items organized in a tree-like structure.
    """
    _items = [dict(item) for item in items]
    _mapping = {}

    for item in _items:
        _mapping.setdefault(item.get(parent_key), []).append(item)

    for item in _items:
        matched = _mapping.get(item.get(primary_key), [])
        # if matched:
        #     item.setdefault(children_key, matched)
        item.setdefault(children_key, matched)

    return _mapping.get("", []) + _mapping.get(None, [])
