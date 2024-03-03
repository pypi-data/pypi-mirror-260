from pysorters.methods import Sorters, gran_array
import pytest


def test_bubble_sort_man():
    sort = Sorters()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.bubble_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_merge_sort_man():
    sort = Sorters()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.merge_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_bubble_sort_gen():
    sort = Sorters()
    array = gran_array()

    sorted_array = sort.bubble_sort(array)
    array.sort()

    assert sorted_array == array


def test_merge_sort_gen():
    sort = Sorters()
    array = gran_array()

    sorted_array = sort.merge_sort(array)
    array.sort()

    assert sorted_array == array
