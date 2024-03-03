from pysorters.methods import Sorters
from pysorters import methods
import random

# Create an instance of the Sorters class
sort = Sorters()

# Create a list of random numbers
array = [random.randint(0, 100) for _ in range(10)]

# Print the unsorted list
print(f"Unsorted list: {array}")

# Sort the list using bubble sort
sorted_array = methods.Sorters.bubble_sort(array)
print(f"Bubble sort: {sorted_array}")

# Sort the list using merge sort
sorted_array = sort.merge_sort(array)
print(f"Merge sort: {sorted_array}")

# Print the representation of the Sorters class
print(sort)
