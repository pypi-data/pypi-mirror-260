import random


class Sorter:
    """Sorter class for sorting arrays using different algorithms"""

    __slots__ = ("array", "__length")

    def __init__(self, array: list = None) -> None:
        """
        Initialize Sorter class
        :param array:
        """
        self.array = array
        self.__length = len(self.array) if self.array else 0

    def quick_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Quicksort algorithm
        :param reverse:
        :type reverse: bool

        :param array:
        :type array: list

        :return list:
        """
        if array is None:
            array: list = self.array if self.array is not None else []

        if len(array) < 2:
            return array

        pivot_index: int = random.randint(0, len(array) - 1)
        pivot: int | float = array[pivot_index]

        less: list = [_ for _ in array if _ < pivot]
        equal: list = [_ for _ in array if _ == pivot]
        greater: list = [_ for _ in array if _ > pivot]

        result = self.quick_sort(less) + equal + self.quick_sort(greater)

        if reverse:
            return result[::-1]

        return result

    def bubble_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Bubble sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array

        for i in range(len(array)):
            for j in range(len(array) - 1):
                if array[j] > array[j + 1]:
                    array[j], array[j + 1] = array[j + 1], array[j]

        if reverse:
            return array[::-1]
        return array

    def merge_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Merge sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array

        if len(array) > 1:
            mid: int | float = len(array) // 2
            left_half: list | float = array[:mid]
            right_half: list | float = array[mid:]

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

        if reverse:
            return array[::-1]
        return array

    def insertion_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Insertion sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array

        for i in range(1, len(array)):
            key = array[i]
            j = i - 1
            while j >= 0 and key < array[j]:
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = key

        if reverse:
            return array[::-1]
        return array

    def selection_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Selection sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array

        for i in range(len(array)):
            min_idx = i
            for j in range(i + 1, len(array)):
                if array[min_idx] > array[j]:
                    min_idx = j
            array[i], array[min_idx] = array[min_idx], array[i]

        if reverse:
            return array[::-1]
        return array

    def counting_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Counting sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array

        max_num = max(array)
        min_num = min(array)

        count = [0] * (max_num - min_num + 1)

        for num in array:
            count[num - min_num] += 1

        z = 0

        for i in range(min_num, max_num + 1):
            for _ in range(count[i - min_num]):
                array[z] = i
                z += 1

        if reverse:
            return array[::-1]
        return array

    def radix_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Radix sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array
        max_num = max(array)

        exp = 1

        while max_num // exp > 0:
            self.counting_sort(array, reverse)
            exp *= 10

        return array

    def bucket_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Bucket sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array
        max_val = max(array)

        bucket = []

        for i in range(len(array)):
            bucket.append([])

        for j in array:
            index_b = int(
                (j / max_val) * (len(array) - 1)
            )  # Adjusted index calculation
            bucket[index_b].append(j)

        for i in range(len(array)):
            if bucket[i]:  # Check if the bucket is not empty
                bucket[i] = self.insertion_sort(bucket[i], reverse)

        k = 0

        for i in range(len(array)):
            for j in range(len(bucket[i])):
                array[k] = bucket[i][j]
                k += 1

        return array

    def tim_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Tim sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array
        array.sort()

        if reverse:
            return array[::-1]

        return array

    def heapify(self, array, n, i):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and array[l] > array[largest]:
            largest = l

        if r < n and array[r] > array[largest]:
            largest = r

        if largest != i:
            array[i], array[largest] = array[largest], array[i]
            self.heapify(array, n, largest)

    def heap_sort(self, array: list = None, reverse: bool = False) -> list:
        """
        Heap sort algorithm
        :param array:
        :type array: list

        :param reverse:
        :type reverse: bool

        :return list:
        """
        array: list = array if array else self.array
        n = len(array)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(array, n, i)
        for i in range(n - 1, 0, -1):
            array[i], array[0] = array[0], array[i]
            self.heapify(array, i, 0)

        if reverse:
            return array[::-1]

        return array

    def __repr__(self) -> str:
        """
        Representation of Sorter class
        :return str:
        """
        return f"{self.__class__.__name__}({self.array})"

    def __str__(self) -> str:
        """
        String representation of Sorter class
        :return str:
        """
        return f"{self.__class__.__name__}({self.array})"

    def __len__(self) -> int:
        """
        Length of Sorter class
        :return int:
        """
        return self.__length

    def __getitem__(self, index) -> int:
        """
        Get item from Sorter class
        :param index:
        :return item:
        """
        return self.array[index]

    def __setitem__(self, index, value) -> None:
        """
        Set item in Sorter class
        :param index:
        :param value:
        :return:
        """
        self.array[index] = value
        self.__length = len(self.array)

    def __delitem__(self, index) -> None:
        del self.array[index]
        self.__length = len(self.array)

    def __contains__(self, item) -> bool:
        return item in self.array


def gran_array_int(
    length: int = 10, start: int = 0, end: int = 100, repeated: bool = True
) -> list:
    gran_arri: list[int] = (
        [random.randint(start, end) for _ in range(length)]
        if repeated
        else list(set([random.randint(start, end) for _ in range(length)]))
    )

    return gran_arri


def gran_array_float(
    length: int = 10, start: int = 0, end: int = 100, repeated: bool = True
) -> list:
    gran_arrf: list[float] = (
        [random.uniform(start, end) for _ in range(length)]
        if repeated
        else list(set([random.uniform(start, end) for _ in range(length)]))
    )

    return gran_arrf


if __name__ == "__main__":  # pragma: no cover
    """Example usage of Sorter class"""
    sort = Sorter()
    array = [random.randint(0, 100) for _ in range(10)]

    print(f"Unsorted list: {array}")

    sorted_array = sort.bubble_sort(array)
    print(f"Bubble sort: {sorted_array}")

    sorted_array = sort.merge_sort(array)
    print(f"Merge sort: {sorted_array}")

    sorted_array = sort.quick_sort(array)
    print(f"Quick sort: {sorted_array}")
