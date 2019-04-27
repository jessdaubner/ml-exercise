# Python Debugging
Debugging a function to correctly calculate the median of the intersection of two sets.

## Solution Efficiency
A more efficient way to find the intersection of two lists is to convert the lists to sets and
use the `intersection` set method. This depulicates the two lists while providing a more efficient
solution than iterating through each list and comparing the elements, which has algorithm efficiency O(N<sup>2</sup>). Additionally, the `statistics`
package, part of the Python standard library, provides a function to calculate the [median](https://github.com/python/cpython/blob/master/Lib/statistics.py#L400-#L421), which uses similar logic and correctly sorts the iterable provided before finding the middle of the data.

## Running the Code
### Unit Tests
Inside the container, run the tests at the command-line with `pytest`. As expected, the two incorrect examples provided should fail for `inner_median` while the tests on the refactored function pass:
```
root@19531ceb560e:/ml-exercise# pytest
================================================================================== test session starts ==================================================================================
platform linux -- Python 3.7.3, pytest-4.4.1, py-1.8.0, pluggy-0.9.0
rootdir: /ml-exercise
collected 11 items

python_debugging/test_python_debugging.py FF.........                                                                                                                             [100%]

======================================================================================= FAILURES ========================================================================================
_________________________________________________________________________ test_inner_median_incorrect_example1 __________________________________________________________________________

    def test_inner_median_incorrect_example1():
>       assert(inner_median([3, 1, 2], [1, 2, 3, 4]) == 2.0)
E       assert 1.0 == 2.0
E        +  where 1.0 = inner_median([3, 1, 2], [1, 2, 3, 4])

python_debugging/test_python_debugging.py:6: AssertionError
_________________________________________________________________________ test_inner_median_incorrect_example2 __________________________________________________________________________

    def test_inner_median_incorrect_example2():
>       assert(inner_median([1, 1, 3, 2, 1, 3], [1, 2, 3, 4]) == 2.0)
E       assert 2.5 == 2.0
E        +  where 2.5 = inner_median([1, 1, 3, 2, 1, 3], [1, 2, 3, 4])

python_debugging/test_python_debugging.py:10: AssertionError
```
### IPython
The code can also be run interactively within the running container as follows:
```
root@a78904fe6a82:/ml-exercise# cd python_debugging/
root@a78904fe6a82:/ml-exercise/python_debugging# ipython
Python 3.7.3 (default, Mar 27 2019, 23:40:30)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.5.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from python_debugging import find_intersection_median

In [2]: find_intersection_median([1, 6, 6, 10], [1, 6])
Out[2]: 3.5
```
