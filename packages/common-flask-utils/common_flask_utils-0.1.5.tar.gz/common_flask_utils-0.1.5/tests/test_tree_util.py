from typing import List

from common_utils.utils.tree_util import from_list


def test_from_list():
    # Test with empty list
    items = []
    result = from_list(items)
    assert result == []

    # Test with a list of items
    items = [
        {"id": 1, "pid": None, "name": "Item 1"},
        {"id": 2, "pid": 1, "name": "Item 2"},
        {"id": 3, "pid": 1, "name": "Item 3"},
        {"id": 4, "pid": 2, "name": "Item 4"},
        {"id": 5, "pid": None, "name": "Item 5"},
    ]
    result = from_list(items)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[0]["name"] == "Item 1"
    assert len(result[0]["children"]) == 2
    assert result[0]["children"][0]["id"] == 2
    assert result[0]["children"][0]["name"] == "Item 2"
    assert len(result[0]["children"][0]["children"]) == 1
    assert result[0]["children"][0]["children"][0]["id"] == 4
    assert result[0]["children"][0]["children"][0]["name"] == "Item 4"
    assert result[0]["children"][1]["id"] == 3
    assert result[0]["children"][1]["name"] == "Item 3"
    assert result[1]["id"] == 5
    assert result[1]["name"] == "Item 5"
    assert len(result[1].get("children", [])) == 0
    assert len(result[1]["children"]) == 0

    # Test with custom keys
    items = [
        {"key": 1, "parent": None, "value": "Item 1"},
        {"key": 2, "parent": 1, "value": "Item 2"},
        {"key": 3, "parent": 1, "value": "Item 3"},
        {"key": 4, "parent": 2, "value": "Item 4"},
        {"key": 5, "parent": None, "value": "Item 5"},
    ]
    result = from_list(
        items, primary_key="key", parent_key="parent", children_key="children"
    )
    assert len(result) == 2
    assert result[0]["key"] == 1
    assert result[0]["value"] == "Item 1"
    assert len(result[0]["children"]) == 2
    assert result[0]["children"][0]["key"] == 2
    assert result[0]["children"][0]["value"] == "Item 2"
    assert len(result[0]["children"][0]["children"]) == 1
    assert result[0]["children"][0]["children"][0]["key"] == 4
    assert result[0]["children"][0]["children"][0]["value"] == "Item 4"
    assert result[0]["children"][1]["key"] == 3
    assert result[0]["children"][1]["value"] == "Item 3"
    assert result[1]["key"] == 5
    assert result[1]["value"] == "Item 5"
    assert len(result[1].get("children", [])) == 0
    assert len(result[1]["children"]) == 0
