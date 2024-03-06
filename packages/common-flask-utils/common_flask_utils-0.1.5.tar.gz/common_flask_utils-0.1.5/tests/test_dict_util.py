from common_utils.utils.dict_util import merge


# Test case 1: Merge two dictionaries without transformation
def test_merge_without_transformation():
    o1 = {"a": 1, "b": 2}
    o2 = {"c": 3, "d": 4}
    expected_result = {"a": 1, "b": 2, "c": 3, "d": 4}
    assert merge(o1, o2) == expected_result


# Test case 3: Merge empty dictionaries
def test_merge_empty_dictionaries():
    o1 = {}
    o2 = {}
    expected_result = {}
    assert merge(o1, o2) == expected_result


# Test case 4: Merge dictionaries with overlapping keys
def test_merge_with_overlapping_keys():
    o1 = {"a": 1, "b": 2}
    o2 = {"b": 3, "c": 4}
    expected_result = {"a": 1, "b": 3, "c": 4}
    assert merge(o1, o2) == expected_result
