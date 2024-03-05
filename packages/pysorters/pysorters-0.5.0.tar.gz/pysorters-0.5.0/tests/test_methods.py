import pytest

from pysorters import Sorter, gran_array_int, gran_array_float


def test_bubble_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.bubble_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_merge_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.merge_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_bubble_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.bubble_sort(array)
    array.sort()

    assert sorted_array == array


def test_merge_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.merge_sort(array)
    array.sort()

    assert sorted_array == array


def test_quick_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.quick_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_quick_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.quick_sort(array)
    array.sort()

    assert sorted_array == array


def test_thunder_methods():
    sort = Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    assert sort.__repr__() == "Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
    assert sort.__str__() == "Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
    assert sort.__len__() == 10
    assert sort.__getitem__(0) == 1
    assert sort.__getitem__(9) == 10
    assert sort.__contains__(5) is True
    assert sort.__contains__(11) is False
    assert sort.__delitem__(0) is None

    sort.__setitem__(0, 1)
    assert sort.__getitem__(0) == 1
    assert sort.__len__() == 9


def test_quick_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.quick_sort(array)
    array.sort()

    assert sorted_array == array


def test_bubble_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.bubble_sort(array)
    array.sort()

    assert sorted_array == array


def test_merge_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.merge_sort(array)
    array.sort()

    assert sorted_array == array


def test_quick_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.quick_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


def test_bubble_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.bubble_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


def test_merge_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.merge_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


if __name__ == "__main__":
    pytest.main()
