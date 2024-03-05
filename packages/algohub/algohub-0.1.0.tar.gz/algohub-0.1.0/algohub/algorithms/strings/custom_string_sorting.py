"""
This module provides functions for string sorting.
"""


from functools import cmp_to_key
from typing import Callable


def sort_items(items: list[str], sorting_fn: Callable[[str, str], int]) -> list[str]:
    """
    Sorts a list of strings using a custom sorting function.

    Parameters:
        items (list[str]): A list of strings to be sorted.
        sorting_fn (Callable[[str, str], int]): A callable function that
         takes two strings as argumentsand returns an integer. This
         function defines the custom sorting logic.

    Returns:
        list[str]: A new list of strings according to the specified sorting function.
    """

    return sorted(items, key=cmp_to_key(sorting_fn))


def compare_vowels_count(text1: str, text2: str) -> int:
    """
    Compares two strings based on the difference in their vowel counts.

    Parameters:
        text1 (str): The first string for comparison.
        text2 (str): The second string for comparison.

    Returns:
        int:
            - A negative value if text1 has fewer vowels than text2.
            - 0 if both texts have the same number of vowels.
            - A positive value if text1 has more vowels than text2.
    """

    vowels_count_1 = sum(1 for char in text1 if char.lower() in 'aeyuio')
    vowels_count_2 = sum(1 for char in text2 if char.lower() in 'aeyuio')
    return vowels_count_1 - vowels_count_2


def compare_chars_sum(text1: str, text2: str) -> int:
    """
    Compares two strings based on the difference in the sum of ASCII values of their characters.

    Parameters:
        text1 (str): The first string for comparison.
        text2 (str): The second string for comparison.

    Returns:
        int:
            - A negative value if the sum of ASCII values in text1 is less than in text2.
            - 0 if both texts have the same sum of ASCII values.
            - A positive value if the sum of ASCII values in text1 is greater than in text2.
    """

    sum_1 = sum(ord(c) for c in text1)
    sum_2 = sum(ord(c) for c in text2)
    return sum_1 - sum_2
