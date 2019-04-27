import pytest
from python_debugging import inner_median, find_intersection_median


def test_inner_median_incorrect_example1():
    assert(inner_median([3, 1, 2], [1, 2, 3, 4]) == 2.0)


def test_inner_median_incorrect_example2():
    assert(inner_median([1, 1, 3, 2, 1, 3], [1, 2, 3, 4]) == 2.0)


def test_inner_median_correct_example1():
    assert(inner_median([1, 3, 2, 1, 3], [1, 2, 3, 4]) == 2.0)


def test_inner_median_raise_assertion():
    with pytest.raises(ValueError):
        inner_median([1], [])


def test_find_intersection_median_incorrect_example1():
    assert(find_intersection_median([3, 1, 2], [1, 2, 3, 4]) == 2.0)


def test_find_intersection_median_incorrect_example2():
    assert(find_intersection_median([1, 1, 3, 2, 1, 3], [1, 2, 3, 4]) == 2.0)


def test_find_intersection_median_correct_example1():
    assert(find_intersection_median([1, 3, 2, 1, 3], [1, 2, 3, 4]) == 2.0)


def test_find_intersection_median_single_intersection():
    assert(find_intersection_median([1, 2, 5], [5, 6, 7]) == 5.0)


def test_find_intersection_median_even_intersection():
    assert(find_intersection_median([11, 13, 18, 21], [21, 13, 18, 11]) == 15.5)


def test_find_intersection_median_odd_intersection():
    assert(find_intersection_median([34, 78, 91, 8], [8, 91, 34]) == 34.0)


def test_find_intersection_median_no_intersection():
    assert(find_intersection_median([1], []) is None)
    assert(find_intersection_median([1, 2, 3], [4, 5, 6]) is None)
