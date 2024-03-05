"""
This module provides various functions for retrieving random number / numbers.
"""

import random
from typing import Callable


def rand_number(min_n: int | float, max_n: int | float) -> int | float:
    """
    Returns an int number or a float number in the range [min_n, max_n]
    Parameters:
        min_n (int|float): The left end of the range
        max_n (int|float): The right end of the range
    Returns:
        int: An int number or a float number in the range [min_n, max_n]
    """

    if min_n > max_n:
        raise ValueError('The range is not correct')
    if (type(min_n), type(max_n)) == (int, int):
        return random.randint(min_n, max_n)
    return random.uniform(min_n, max_n)


def rand_number_until(min_n: int | float,
                      max_n: int | float,
                      condition_fn: Callable[[int | float], bool]) -> int | float:
    """
    Returns an int number or a float number in the range [min_n, max_n]
     untils it meets the condition
    Parameters:
        min_n (int|float): The left end of the range
        max_n (int|float): The right end of the range
        condition_fn (Callable[[int|float],bool]): The condition function
    Returns:
        int: An int number or a float number in the range [min_n, max_n]
        that satisfies the condition
    """

    if min_n > max_n:
        raise ValueError('The range is not correct')

    if (type(min_n), type(max_n)) == (int, int):
        return _rand_number_until(min_n, max_n, condition_fn, int)

    return _rand_number_until(min_n, max_n, condition_fn, float)


def rand_chr(min_c: str, max_c: str) -> str:
    """
    Returns a char in the range [min_chr, max_chr]
    Parameters:
        min_c (str): The left end of the range
        max_c (str): The right end of the range
    Returns:
        str: A char in the range [min_c, max_c]

    """
    return chr(rand_number(ord(min_c), ord(max_c)))


def rand_chr_until(min_c: str, max_c: str, condition_fn: Callable[[str], bool]) -> str:
    """
    Returns a char in teh range [min_chr, max_chr] until it mets the condition
    Parameters:
        min_c (str): The left end of the range
        max_c (str): The right end of the range
        condition_fn (Callable[[str],bool]): The condition function
    Returns:
        str: A char in the range [min_c, max_c] that satisfies the condition
    """

    while not condition_fn(c := rand_chr(min_c, max_c)):
        pass
    return c


def rand_n_numbers(n: int, min_n: int | float, max_n: int | float) -> list[int] | list[float]:
    """
    Returns list of int numbers or  float numbers in the range [min_n, max_n]
    Parameters:
        n (int): The number of itmes
        min_n (int|float): The left end of the range
        max_n (int|float): The right end of the range
    Returns:
        list[int]: A list containing int numbers or a float numbers in the range [min_n, max_n]
    """
    if n <= 0:
        raise ValueError('THe number of items is not corect')

    if min_n > max_n:
        raise ValueError('The range is not correct')

    if (type(min_n), type(max_n)) == (int, int):
        return [random.randint(min_n, max_n) for _ in range(n)]

    return [random.uniform(min_n, max_n) for _ in range(n)]


def rand_n_numbers_until(n, min_n: int | float,
                         max_n: int | float,
                         condition_fn: Callable[[int | float], bool]) \
        -> list[int] | list[float]:
    """
    Returns int numbers or float numbers in the range [min_n, max_n] untils
     it meets the condition
    Parameters:
        n (int): The number of items
        min_n (int|float): The left end of the range
        max_n (int|float): The right end of the range
        condition_fn (Callable[[int|float],bool]): The condition function
    Returns:
        list[int|float]: Int numbers or float numbers in the range [min_n, max_n]
         that satisfies the condition
    """

    if n <= 0:
        raise ValueError('THe number of items is not corect')

    if min_n > max_n:
        raise ValueError('The range is not correct')

    if (type(min_n), type(max_n)) == (int, int):
        return [_rand_number_until(min_n, max_n, condition_fn, int) for _ in range(n)]

    return [_rand_number_until(min_n, max_n, condition_fn, float)]


def _rand_number_until(
        min_n: int, max_n: int,
        condition_fn: Callable[[int | float], bool],
        data_type: type) \
        -> int | float:
    if data_type == int:
        while not condition_fn(v := random.randint(min_n, max_n)):
            pass
        return v

    while not condition_fn(v := random.uniform(min_n, max_n)):
        pass
    return v
