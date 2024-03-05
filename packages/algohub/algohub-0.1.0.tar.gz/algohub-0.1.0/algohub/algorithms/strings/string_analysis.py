"""
This module provides functions for string analysis.
"""

from collections import Counter
from typing import Any


def is_anagram(text1: str, text2: str) -> bool:
    """
    Checks if two strings are anagrams of each other.
    An anagram is a word of phrase formed by rearranging the letters of a different word or phrase

    Parameters:
        text1 (str): The first string to check
        text2 (str): The second string to check
    Returns:
        bool: True if the strings are anagrams, False otherwise
    """

    if len(text1) != len(text2):
        return False
    return Counter(text1) == Counter(text2)


def is_pangram(text: str) -> bool:
    """
    Checks if a string is a pangram.
    A pangram is a sentence or phrase that contains every letter of the alphabet at least once.

    Parameters:
        text (str): The string to check.

    Returns:
        bool: True if the string is a pangram, False otherwise.
    """

    return len({c.lower() for c in text if c.isalpha()}) == 26


def is_palindrome(text: str) -> bool:
    """
    Checks if the given text is a palindrome.

    A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and
    removing all non-alphanumeric characters, it reads the same forward and backward.

    Parameters:
        text (str): The text to be checked for palindrome.

    Returns:
        bool: True if the text is a palindrome, False otherwise.
    """

    cleaned_text = ''.join(c.lower() for c in text if c.isalnum())
    start_index = 0
    end_index = len(cleaned_text) - 1
    while start_index < end_index:
        if cleaned_text[start_index] != cleaned_text[end_index]:
            return False
        start_index += 1
        end_index -= 1
    return True


def is_potential_palindrome(text: str) -> bool:
    """
    Checks if the given string can be rearranged to form a palindrome.

    Parameters:
        text (str): The text to be checked for potential palindrome.

    Returns:
        bool: True if the text can be rearranged to form a palindrome, False otherwise.
    """

    cleaned_text = ''.join(c.lower() for c in text if c.isalnum())
    chars_counter = Counter(cleaned_text)
    odd_count = sum(count % 2 for count in chars_counter.values())
    return odd_count <= 1


def is_subsequence(text: str, subsequence: str) -> bool:
    """
    Checks if a given text contains the specified subsequence.

    Parameters:
        text (str): The text to be searched for the subsequence.
        subsequence (str): The subsequence to check in the text.

    Returns:
        bool: True if the subsequence is present, False otherwise.
    """

    if not subsequence:
        return True

    sub_index = 0
    for c in text:
        if sub_index < len(subsequence) and c.lower() == subsequence[sub_index].lower():
            sub_index += 1
            if sub_index == len(subsequence):
                return True
    return False


def is_substring(text: str, substring: str) -> bool:
    """
    Checks if a given text contains the specified substring.

    Parameters:
        text (str): The text to be searched for the substring.
        substring (str): The substring to check in the text.

    Returns:
        bool: True if the substring is present, False otherwise.
    """

    lowercase_text = [c.lower() for c in text]
    lowercase_substring = [c.lower() for c in substring]

    if lowercase_substring == lowercase_text:
        return True
    if len(lowercase_substring) > len(lowercase_text):
        return False

    for i in range(len(text) - len(substring) + 1):
        if lowercase_text[i:i + len(lowercase_substring)] == lowercase_substring:
            return True
    return False


def count_substring_occurences(text: str, substring: str) -> int:
    """
    Counts the number of occurrences of a substring within a given text.

    Parameters:
        text (str): The text in which occurrences of the substring will be counted.
        substring (str): The substring to be counted within the text.

    Returns:
        int: The number of occurrences of the substring in the text.
    """

    count = 0
    lowercase_text = [c.lower() for c in text]
    lowercase_substring = [c.lower() for c in substring]
    for i in range(len(lowercase_text)):
        if lowercase_text[i:i + len(lowercase_substring)] == lowercase_substring:
            count += 1
    return count


def contains_duplicates(items: list[Any]) -> bool:
    """
    Checks if a list of items contains any duplicates.

    Parameters:
        items (list[Any]): List of items.

    Returns:
        bool: True if duplicates are found, False otherwise.
    """

    unique_elements = set(item.lower() if isinstance(item, str) else item for item in items)
    if len(unique_elements) == len(items):
        return False
    return True
