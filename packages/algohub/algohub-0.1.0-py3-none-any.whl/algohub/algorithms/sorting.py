"""
This module provides several classes for sorting.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class Sorting(ABC):
    """
    An abstract base class for sorting algorithms.
    """

    @abstractmethod
    def sort(self, data: list[Any]) -> list[Any]:
        """
        Sorts a list of elements.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """
        pass


class QuickSort(Sorting):
    """
    A class implementing the QuickSort algorithm, a divide-and-conquer sorting algorithm
    """

    def sort(self, data: list[Any]) -> list[Any]:
        """
        Sorts a list using the QuickSort algorithm.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """

        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        less_than_pivot = [x for x in data if x < pivot]
        greater_than_pivot = [x for x in data if x > pivot]
        equal_to_pivot = [x for x in data if x == pivot]
        return self.sort(less_than_pivot) + equal_to_pivot + self.sort(greater_than_pivot)


class BubbleSort(Sorting):
    """
    A class implementing the BubbleSort algorithm
    """

    def sort(self, data: list[Any]) -> list[Any]:
        """
        Sorts a list using the BubbleSort algorithm.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """

        sorted_data = data.copy()
        for i in range(len(sorted_data)):
            for j in range(0, len(sorted_data) - i - 1):
                if sorted_data[j] > sorted_data[j + 1]:
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]
        return sorted_data


class MergeSort(Sorting):
    """
    A class implementing the MergeSort algorithm
    """

    @staticmethod
    def merge(left_half: list[int], right_half: list[int]) -> list[int]:
        """
        Merges two sorted lists into a single sorted list.

        Parameters:
            left_half : list[int]
                The left half of the split list.
            right_half : list[int]
                The right half of the split list.

        Returns:
            list[int]
                The merged and sorted list.
        """

        merged = []
        i = j = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                merged.append(left_half[i])
                i += 1
            else:
                merged.append(right_half[j])
                j += 1

        merged.extend(left_half[i:])
        merged.extend(right_half[j:])
        return merged

    def sort(self, data: list[Any]) -> list[Any]:
        """
        Sorts a list using the MergeSort algorithm.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """

        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left_half = self.sort(data[:mid])
        right_half = self.sort(data[mid:])
        return MergeSort.merge(left_half, right_half)


class SelectionSort(Sorting):
    """
    A class implementing the SelectionSort algorithm
    """

    def sort(self, data: list[Any]) -> list[Any]:
        """
        Sorts a list using the SelectionSort algorithm.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """

        sorted_data = data.copy()
        for i in range(len(sorted_data) - 1):
            min_index = i
            for j in range(i + 1, len(sorted_data)):
                if sorted_data[j] < sorted_data[min_index]:
                    min_index = j
            sorted_data[i], sorted_data[min_index] = sorted_data[min_index], sorted_data[i]
        return sorted_data


@dataclass
class SortingManager:
    """
    A class that manages the sorting strategy and performs sorting using the specified strategy.
    """
    sorting_strategy: Sorting = QuickSort()

    def set_sorting_strategy(self, sorting_strategy: Sorting):
        """
        Sets the sorting strategy to be used.

        Parameters:
            sorting_strategy : Sorting
                The sorting strategy to be set.
        """

        self.sorting_strategy = sorting_strategy

    def perform_sorting(self, data: list[Any]) -> list[Any]:
        """
        Performs sorting on a list using the current sorting strategy.

        Parameters:
            data : list[Any]
                The list of elements to be sorted.

        Returns:
            list[Any]
                The sorted list.
        """

        return self.sorting_strategy.sort(data)
