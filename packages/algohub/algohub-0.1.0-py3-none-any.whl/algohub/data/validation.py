"""
This module provides various functions for data validation.
"""

import re
from collections import Counter
from typing import Callable


def does_number_meet_condition(n: int, condition_fn: Callable[[int], bool]) -> bool:
    """
    Checks if a number meets a specified condition.

    Parameters:
        n (int): The number to be checked.
        condition_fn (Callable[[int], bool]): A condition function to check if is met by number.

    Returns:
        bool: True if the number meets the condition, otherwise False.
    """

    return condition_fn(n)


def is_number_within_range(number: int, r_min: int, r_max: int) -> bool:
    """
    Checks if a number is within a specified range.

    Parameters:
        number (int): The number to be checked.
        r_min (int): The minimum value of the range.
        r_max (int): The maximum value of the range.

    Returns:
        bool: True if the number is within the range, otherwise False.

    Raises:
        ValueError: If the range is not correct (r_min > r_max).
    """

    if r_min > r_max:
        raise ValueError('The range is not correct')
    return r_min <= number <= r_max


def does_number_match_regex(
        n: int,
        data_type: int | float,
        regex: str | None = None) \
        -> int | float:
    """
    Checks if a number matches a specified regular expression pattern
     based on its data type.

    Parameters:
        n (int | float): The number to be checked.
        data_type (int | float): The type of the number (int or float).
        regex (str, optional): Regular expression pattern to match against.
            If not provided, a default pattern based on the data type will be used.

    Returns:
        int | float: True if number matches the specified regular
         expression pattern, otherwise False.

    Raises:
        TypeError: If data_type is not int or float.
    """

    if data_type not in [int, float]:
        raise TypeError('Incorrect type')

    data_type_regex = {
        int: r'^-?\d+(\.0+)?$',
        float: r'^-?\d+\.\d+$'
    }

    data_regex = regex if regex else data_type_regex[data_type]
    if not re.match(data_regex, str(n)):
        return False
    return True


def does_text_meet_condition(text: str, condition_fn: Callable[[str], bool]) -> bool:
    """
    Checks if text meets a specified condition.

    Parameters:
        text (str): The text to be checked.
        condition_fn (Callable[[str], bool]): A condition function defining to check if is met by text.

    Returns:
        bool: True if the text meets the condition, otherwise False.
    """

    return condition_fn(text)


def does_text_meet_char_count(text: str, char: str, expected_count: int) -> bool:
    """
    Checks if a text contains a specified character a certain number of times.

    Parameters:
        text (str): The text to be checked.
        char (str): The character to be counted.
        expected_count (int): The expected count of the character.

    Returns:
        bool: True if the text meets the character count, otherwise False.
    """

    if char not in text:
        return False
    count = sum(1 for c in text if c == char)
    return count == expected_count


def does_text_meet_characters_count(
        text: str,
        expected_chars_count: dict[str, int]
) -> bool:
    """
    Checks if a text contains specified characters with specified counts.

    Parameters:
        text (str): The text to be checked.
        expected_chars_count (dict[str, int]): A dictionary specifying the characters
            and their expected counts.

    Returns:
        bool: True if the text meets the character counts, otherwise False.
    """

    chars_count = Counter(text)
    return expected_chars_count == chars_count


def does_text_meet_characters_count_allow_additional(
        text: str,
        expected_chars_count: dict[str, int]
) -> bool:
    """
    Checks if a text contains specified characters with specified counts,
    allowing additional characters.

    Parameters:
        text (str): The text to be checked.
        expected_chars_count (dict[str, int]): A dictionary specifying the characters
            and their expected counts.

    Returns:
        bool: True if the text meets the character counts while allowing additional characters,
            otherwise False.
    """

    chars_count = Counter(text)
    for char, count in expected_chars_count.items():
        if chars_count[char] < count:
            return False
    return True


def does_string_match_regex(text: str, pattern: str = r'^[A-Z][a-z]+$') -> bool:
    """
    Checks if a string matches a specified regular expression pattern.

    Parameters:
        text (str): The string to be checked.
        pattern (str, optional): Regular expression pattern to match against.
            The default pattern checks if the string follows a specific naming convention where
            the first letter is capitalized and the rest are lowercase.

    Returns:
        bool: True if the string matches the specified regular expression pattern, otherwise False.
    """

    if re.match(pattern, text):
        return True
    return False


def does_char_fall_within_range(char: str, min_char: str, max_char: str) -> bool:
    """
    Checks if a character falls within a specified range.

    Parameters:
        char (str): The character to be checked.
        min_char (str): The minimum value of the range.
        max_char (str): The maximum value of the range.

    Returns:
        bool: True if the character falls within the range, otherwise False.

    Raises:
        ValueError: If the length of char is not equal to 1 or if the range
        is not correct (ord(min_char) > ord(max_char)).
    """

    if len(char) != 1:
        raise ValueError('Char must consist of one letter')
    if ord(min_char) > ord(max_char):
        raise ValueError('The range is not correct')
    return min_char <= char <= max_char
