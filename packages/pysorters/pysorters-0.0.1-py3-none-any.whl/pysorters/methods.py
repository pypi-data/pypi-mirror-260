import random


class Sorters:
    """Sorters class for sorting arrays"""

    __slots__ = ("array", "__length")

    def __init__(self, array: list = None):
        """
        Initialize Sorters class
        :param array:
        """
        self.array = array if array else []
        self.__length = len(self.array)  # Use self.array instead of array

    def quicksort(self, array: list) -> list:
        """
        Quicksort algorithm
        :param array:
        :return list:
        """
        if len(array) < 2:
            return array
        else:
            pivot = array[0]
            less = [i for i in array[1:] if i <= pivot]
            greater = [i for i in array[1:] if i > pivot]

            return self.quicksort(less) + [pivot] + self.quicksort(greater)

    @staticmethod
    def bubble_sort(array) -> list:
        """
        Bubble sort algorithm
        :param array:
        :return list:
        """
        for i in range(len(array)):
            for j in range(len(array) - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def merge_sort(self, array: list) -> list:
        """
        Merge sort algorithm
        :param array:
        :return list:
        """
        if len(array) > 1:
            mid = len(array) // 2
            left_half = array[:mid]
            right_half = array[mid:]

            self.merge_sort(left_half)
            self.merge_sort(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    array[k] = left_half[i]
                    i += 1
                else:
                    array[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                array[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                array[k] = right_half[j]
                j += 1
                k += 1

        return array

    def __repr__(self):
        """
        Representation of Sorters class
        :return str:
        """
        return f"{self.__class__.__name__}({self.array})"

    def __str__(self):
        """
        String representation of Sorters class
        :return str:
        """
        return f"{self.__class__.__name__}({self.array})"

    def __len__(self):
        """
        Length of Sorters class
        :return int:
        """
        return self.__length

    def __iter__(self):
        """
        Iterator of Sorters class
        :return iter:
        """
        return iter(self.array)

    def __getitem__(self, index):
        """
        Get item from Sorters class
        :param index:
        :return item:
        """
        return self.array[index]

    def __setitem__(self, index, value):
        """
        Set item in Sorters class
        :param index:
        :param value:
        :return:
        """
        self.array[index] = value
        self.__length = len(self.array)

    def __delitem__(self, index):
        del self.array[index]
        self.__length = len(self.array)

    def __contains__(self, item):
        return item in self.array


def gran_array(length: int = 10, start: int = 0, end: int = 100) -> list:
    gran_arr: list[int] = [random.randint(start, end) for _ in range(length)]

    return gran_arr


if __name__ == "__main__":
    """Example usage of Sorters class"""
    sort = Sorters()
    array = [random.randint(0, 100) for _ in range(10)]

    print(f"Unsorted list: {array}")

    sorted_array = sort.bubble_sort(array)
    print(f"Bubble sort: {sorted_array}")

    sorted_array = sort.merge_sort(array)
    print(f"Merge sort: {sorted_array}")

    print(sort)
