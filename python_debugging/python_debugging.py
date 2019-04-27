"""
Contains the initial buggy function inner_median to be debugged
and the refactored function find_intersection_median.
"""
import logging
from statistics import median


def inner_median(x, y):
    """
    Returns the median of the set intersection of two lists of integers. Ex:
    inner_median([1,2,3], [2,3,3]) would return 2.5 ([2,3] is the intersection
    of x, y and 2.5 is the median of [2,3]).
    x (list<int>): A list of integers.
    y (list<int>): A list of integers.
    """
    intersection = []
    # get intersection set
    for x_val in x:
        for y_val in y:
            if y_val == x_val:
                intersection.append(x_val)
    # no intersection
    if len(intersection) == 0:
        raise ValueError("There were no common elements in x, y")
    # odd: get mid-point
    elif len(intersection) % 2 != 0:
        return float(intersection[int(len(intersection) / 2)])
    # even: average mid-points
    else:
        mid_a = intersection[int(len(intersection) / 2) - 1]
        mid_b = intersection[round(len(intersection) / 2)]
        return float(mid_a + mid_b) / 2


def find_intersection_median(x, y):
    """Finds the median of the set intersection of two lists of integers. Ex:
       find_intersection_median([1, 2, 3], [2, 3, 3]) would return 2.5 ([2, 3]
       is the intersection of x, y and 2.5 is the median of [2, 3]).
    Args:
      x (list<int>): A list of integers.
      y (list<int>): A list of integers.
    Returns:
        Median as float or None if no intersection exists
    """
    set_x = set(x)
    set_y = set(y)
    set_intersection = set_x.intersection(set_y)

    if not set_intersection:
        logging.warning("No common elements in x and y")
        return None

    return float(median(set_intersection))
