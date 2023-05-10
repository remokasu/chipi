from typing import Any, List, Callable
import csv
import json


"""
The Buffer class provides a simple interface for managing a buffer of data. It can be used for storing, adding,
deleting, and performing various operations on data. 

Usage:
    from buffer_classes import Buffer, BufferManager

    buf = Buffer("example_buffer")
    buf.add(1)
    buf.add(2)
    buf.add(3)

Available methods:

1. add(value) - Adds a value to the end of the buffer.
2. delete(index) - Deletes a value at the given index from the buffer.
3. clear() - Clears the buffer, removing all its contents.
4. delta() - Returns the numeric difference between the first and last values of the buffer.
5. find_duplicate(value) - Returns the index of the first duplicate occurrence of the given value.
6. point_diff(index1, index2) - Returns the numeric difference between two values at given indices.
7. has_difference() - Returns True if there is a numeric difference between any two consecutive values, otherwise False.
8. has_non_numeric_difference() - Returns True if there is a non-numeric difference between any two consecutive values, otherwise False.
9. reverse() - Reverses the order of the buffer's data.
10. sort(reverse=False) - Sorts the buffer's data in ascending (default) or descending order.
11. filter(function) - Filters the buffer's data using a custom function and returns a new list of filtered data.
12. resample(step) - Resamples the buffer's data with a given step size and returns a new list of resampled data.
13. slice(start, end) - Slices the buffer's data from the given start index to the end index and returns a new list of sliced data.
14. find(function) - Returns the index of the first element that satisfies the given function, otherwise -1.
15. max_value() - Returns the maximum numeric value in the buffer.
16. min_value() - Returns the minimum numeric value in the buffer.
17. mean() - Returns the mean of the numeric values in the buffer.
18. unique() - Returns a new list of unique values in the buffer, in the order they were first encountered.

Note: The BufferManager class provides additional functionality for managing multiple Buffer objects.
"""


class Buffer:
    def __init__(self, label: str, max_size: int = 65535) -> None:
        """
        Initialize the buffer with a label and optional max size.

        Args:
            label (str): The name of the buffer.
            max_size (int, optional): The maximum size of the buffer. Defaults to 65535.
        """
        self.label = label
        self.arr: List[Any] = []
        self._max_size = max_size

    def __call__(self, index: int) -> Any:
        """
        Get the value at a specific index in the buffer.

        Args:
            index (int): The index of the desired value.

        Returns:
            Any: The value at the specified index.
        """
        return self.arr[index]

    def set_max_len(self, value: int) -> None:
        """
        Set the maximum size of the buffer.

        Args:
            value (int): The new maximum size of the buffer.
        """
        self._max_size = int(value)

    def add(self, value: Any) -> None:
        """
        Append a value to the buffer. If the buffer is at its maximum size,
        remove the first element before appending.

        Args:
            value (Any): The value to be appended.
        """
        if self.len == self._max_size:
            self.arr.pop(0)
        self.arr.append(value)

    @property
    def previous_value(self) -> Any:
        """
        Get the previous value in the buffer.

        Returns:
            Any: The previous value or None if the buffer has fewer than 2 elements.
        """
        if self.len >= 2:
            return self.arr[-2]
        else:
            return None

    @property
    def current_value(self) -> Any:
        """
        Get the current (latest) value in the buffer.

        Returns:
            Any: The current value or None if the buffer is empty.
        """
        return self.arr[-1] if self.arr else None

    def clear(self) -> None:
        """
        Clear the buffer by initializing it as an empty list.
        """
        self.arr = []

    def replace(self, arr: List[Any]) -> None:
        """
        Replace the current buffer with a new list.

        Args:
            arr (List[Any]): The new list to replace the current buffer.
        """
        self.clear()
        self.arr = arr.copy()

    @property
    def len(self) -> int:
        """
        Get the length of the buffer.

        Returns:
            int: The length of the buffer.
        """
        return len(self.arr)

    @property
    def data(self) -> List[Any]:
        """
        Get the buffer's data as a list.

        Returns:
            List[Any]: The buffer's data.
        """
        return self.arr

    def value(self, index: int) -> None:
        """
        Get the value at a specific index in the buffer.

        Args:
            index (int): The index of the desired value.

        Returns:
            Any: The value at the specified index.
        """
        return self.arr[index]

    def delete(self, index: int) -> None:
        """
        Delete the value at a specific index in the buffer.

        Args:
            index (int): The index of the value to be deleted.
        """
        self.arr.pop(index)

    @property
    def is_empty(self) -> bool:
        """
        Check if the buffer is empty or not.

        Returns:
            bool: True if the buffer is empty, otherwise False.
        """
        return len(self.arr) == 0

    def find_duplicate(self, value: Any) -> int:
        """
        Find the index of a duplicate value in the buffer, if it exists.

        Args:
            value (Any): The value to search for duplicates.

        Returns:
            int: The index of the duplicate value or -1 if not found.
        """
        for i in range(len(self.arr)):
            if self.arr[i] == value:
                return i
        return -1

    def delta(self) -> Any:
        """
        Calculate the difference between the current and previous values in the buffer.

        Returns:
            Any: The difference between the current and previous values.
        """
        return self.current_value - self.previous_value

    def point_diff(self, idx_pre: int, idx_now: int) -> Any:
        """
        Calculate the difference between two values in the buffer, given their indices.

        Args:
            idx_pre (int): The index of the first value.
            idx_now (int): The index of the second value.

        Returns:
            Any: The difference between the two values at the given indices.
        """
        return self.arr[idx_now] - self.arr[idx_pre]

    def has_difference(self, epsilon: float | None = None) -> bool:
        """
        Check if there is a difference between the current and previous values in the buffer.

        Args:
            epsilon (float | None, optional): If set, compare the values with this tolerance
                for floating-point error. Defaults to None.

        Returns:
            bool: True if there is a difference, otherwise False.
        """
        if len(self.arr) >= 2:
            if epsilon is None:
                return self.previous_value != self.current_value
            else:
                return abs(self.previous_value - self.current_value) > epsilon
        else:
            return False

    def has_non_numeric_difference(self) -> bool:
        """
        Check if there is a difference between the current and previous non-numeric values in the buffer.

        Returns:
            bool: True if there is a difference, otherwise False.
        """
        if len(self.arr) >= 2:
            return self.previous_value != self.current_value
        else:
            return False

    def reverse(self) -> None:
        """Reverse the order of data in the buffer."""
        self.arr.reverse()

    def sort(self, key: Callable[[Any], Any] = None, reverse: bool = False) -> None:
        """Sort the data in the buffer according to the specified criteria.

        Args:
            key (Callable[[Any], Any], optional): A function that takes an element as input and returns a value used to determine the sort order. Defaults to None.
            reverse (bool, optional): If set to True, the data will be sorted in descending order. Defaults to False.
        """
        self.arr.sort(key=key, reverse=reverse)

    def filter(self, filter_func: Callable[[Any], bool]) -> List[Any]:
        """Filter the data in the buffer using a custom filter function.

        Args:
            filter_func (Callable[[Any], bool]): A function that takes an element as input and returns a boolean.

        Returns:
            List[Any]: A list of filtered elements.
        """
        return list(filter(filter_func, self.arr))

    def resample(self, step: int) -> List[Any]:
        """Resample the data in the buffer by selecting every 'step' elements.

        Args:
            step (int): The step size to use when selecting elements.

        Returns:
            List[Any]: A list of resampled elements.
        """
        return self.arr[::step]

    def slice(self, start: int, end: int, step: int = 1) -> List[Any]:
        """Return a slice of the data in the buffer.

        Args:
            start (int): The starting index of the slice.
            end (int): The ending index of the slice.
            step (int, optional): The step between items in the slice. Defaults to 1.

        Returns:
            List[Any]: A list of sliced items.
        """
        return self.arr[start:end:step]

    def find(self, condition_func: Callable[[Any], bool]) -> int:
        """Find the index of the first item in the buffer that meets the given condition.

        Args:
            condition_func (Callable[[Any], bool]): A function that takes an item and returns
                True if the item meets the condition, otherwise False.

        Returns:
            int: The index of the found item or -1 if not found.
        """
        for i, item in enumerate(self.arr):
            if condition_func(item):
                return i
        return -1

    def max_value(self) -> Any:
        """Get the maximum value in the buffer."""
        return max(self.arr)

    def min_value(self) -> Any:
        """Get the minimum value in the buffer."""
        return min(self.arr)

    def mean(self) -> float:
        """Calculate the mean of the data in the buffer."""
        return sum(self.arr) / len(self.arr)

    def unique(self) -> List[Any]:
        """Return a list of unique elements in the buffer."""
        return list(set(self.arr))

    def export_to_csv(self, file_path: str, delimiter: str = ',') -> None:
        """Export the data in the buffer to a CSV file.

        Args:
            file_path (str): The file path to save the CSV file.
            delimiter (str, optional): The delimiter used in the CSV file. Defaults to ','.
        """
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=delimiter)
            for item in self.arr:
                csv_writer.writerow([item])


class BufferManager:
    """
    A class for managing multiple buffers.
    Args:
        labels (List[str]): A list of buffer names.

    Example:
        # create buffer
        buff = Buffer(["data1", "data2", "data3"])

        # add data
        buff.d["data1"].add(x)
        buff.d["data2"].add(x)
        buff.d["data3"].add(x)
    """

    def __init__(self, labels: List[str]) -> None:
        self.labels = labels
        self.num_buff = len(self.labels)
        self.d = {label: Buffer(label) for label in self.labels}

    def clear(self, label: str) -> None:
        """
        Clear all data from the specified buffer.

        Args:
            label (str): The target buffer label.
        """
        self.d[label].clear()

    def get_data(self, label: str) -> List[Any]:
        """Get data from the specified buffer.

        Args:
            label (str): The target buffer label to get data from.

        Returns:
            List[Any]: The data from the specified buffer.
        """
        return self.d[label].data

    def copy_data(self, source_label: str, target_label: str) -> None:
        """Copy data from one buffer to another."""
        self.d[target_label].replace(self.d[source_label].data)

    def move_data(self, source_label: str, target_label: str) -> None:
        """Move data from one buffer to another and clear the source buffer."""
        self.copy_data(source_label, target_label)
        self.clear(source_label)

    def import_from_json(self, label: str, file_path: str) -> None:
        """Import data from a JSON file into the specified buffer.

        Args:
            label (str): The target buffer label to import data into.
            file_path (str): The file path to read the JSON file.
        """
        with open(file_path, 'r') as jsonfile:
            data = json.load(jsonfile)
            self.d[label].replace(data)

    def export_to_json(self, label: str, file_path: str) -> None:
        """Export data from the specified buffer to a JSON file.

        Args:
            label (str): The target buffer label to export data from.
            file_path (str): The file path to write the JSON file.
        """
        with open(file_path, 'w') as jsonfile:
            json.dump(self.d[label].data, jsonfile)
