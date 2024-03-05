"""
This module provides functions for working with divisors of integers.
"""

import math


def count_divisors(n: int) -> int | float:
    """
    Counts the number of divisors for a given integer.

    Parameters:
        n (int): The integer for which to count divisors.

    Returns:
        int | float: The number of divisors.
    """

    if n == 0:
        return float('inf')
    nn = abs(n) if n < 0 else n

    divisors_counter = {1: 1, 2: 2, 3: 2}
    if nn in divisors_counter:
        return divisors_counter[nn]
    counter = 2
    i = 2
    while i * i < nn:
        if nn % i == 0:
            counter += 2
        i += 1
    if i * i == nn:
        counter += 1
    return counter


def count_common_divisors(a: int, b: int) -> int | float:
    """
    Calculates the number of common divisors for the given integers.

    Parameters:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int | float: The common number of divisors for the integers.
    """

    if a == 0 and b == 0:
        return float('inf')
    if a == 0 and b != 0:
        return count_divisors(b)
    if a != 0 and b == 0:
        return count_divisors(a)
    return count_divisors(math.gcd(a, b))


def sum_divisors(n: int, n_included: bool = True) -> int | float:
    """
    Calculates and returns the sum of divisors for the given integer.

    Parameters:
        n (int): Number for which the sum of divisors is determined.
        n_included (bool): Indicates whether the number n will be
         taken into account when summing the divisors.

    Returns:
        int | float: The sum of divisors for the integer, or infinity if the integer is 0.
    """

    if n == 0:
        return float('inf')
    nn = abs(n) if n < 0 else n
    divisors_sum = {1: 1, 2: 3, 3: 4}
    if nn in divisors_sum:
        return divisors_sum[nn]
    sum_of_divisors = (nn if n_included else 0) + 1
    i = 2
    while i * i < nn:
        if nn % i == 0:
            sum_of_divisors += (i + (nn // i))
        i += 1
    if i * i == nn:
        sum_of_divisors += i
    return sum_of_divisors
