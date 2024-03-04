import random

from pysorters.methods import Sorter

# Create an instance of the Sorter class
print(
    """
Welcome to PySorters!
This is a package that contains all sorting algorithms.
- You can use the Sorter class to sort your lists.
- You can use the gran_array_int function to generate a random list.

Example usage of Sorter class:
sort = Sorter()
array = [random.randint(0, 100) for _ in range(10)]

print(f"Unsorted list: {array}")

sorted_array = sort.bubble_sort(array)
print(f"Bubble sort: {sorted_array}")

sorted_array = sort.merge_sort(array)
print(f"Merge sort: {sorted_array}")

sorted_array = sort.quick_sort(array)
print(f"Quick sort: {sorted_array}")
"""
)

sort = Sorter()
array = [random.randint(0, 100) for _ in range(10)]

print(f"Unsorted list: {array}")

sorted_array = sort.bubble_sort(array)
print(f"Bubble sort: {sorted_array}")

sorted_array = sort.merge_sort(array)
print(f"Merge sort: {sorted_array}")

sorted_array = sort.quick_sort(array)
print(f"Quick sort: {sorted_array}")
