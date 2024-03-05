"""
This module provides functions for various mathematical algorithms,
"""


def binary_search(numbers: list[int], looked_number: int) -> int | bool:
    """
    Performs binary search to find the index of the looked number in the sorted list of numbers

    Parameters:
        numbers (list[int]): A sorted list of integers.
        looked_number (int): The integer to be found in the list.

    Returns:
        int | bool: If the looked_number is found in the list, returns the index of the number,
        otherwise False.
    """

    if not numbers:
        return False
    first_index = 0
    end_index = len(numbers) - 1
    while first_index <= end_index:
        middle_element_index = (first_index + end_index) // 2
        if looked_number == numbers[middle_element_index]:
            return middle_element_index
        if looked_number < numbers[middle_element_index]:
            end_index = middle_element_index - 1
        else:
            first_index = middle_element_index + 1
    return False


def babylonian_sqrt(n: int, accuracy: float = 0.001) -> float:
    """
    Calculates the square root of a number using the Babylonian method.

    Parameters:
        n (int): The number for which the square root is to be calculated.
        accuracy (float): The level of precision for the approximation. Defaults to 0.001.

    Returns:
        float: The approximate square root of the number.
    """

    r = n
    #     r: float = n  # Declaring r as float
    while abs(n - r * r) > accuracy:
        r = (r + n / r) / 2
    return round(r, 3)


def binary_exponentiation(number: int, power: int) -> int:
    """
    Computes the result of raising a given number to the power using binary exponentiation.

    Parameters:
        number (int): The base number.
        power (int): The exponent to which the base number is raised.

    Returns:
        int: The result of raising number to the power.
    """

    result = 1
    while power > 0:
        if power % 2 == 1:
            result *= number
        number *= number
        power //= 2
    return result


def iterative_factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer using an iterative approach.

    Parameters:
        n (int): The non-negative integer for which to calculate the factorial.

    Returns:
        int: The factorial of the integer.

    Raises:
        ValueError: If n is a negative number.
    """

    if n < 0:
        raise ValueError('The number must be a non-negative integer')
    if n in [0, 1]:
        return 1

    product = 1
    while n > 1:
        product *= n
        n -= 1
    return product


def recursive_factorial(n: int) -> int:
    """
    Calculates the factorial of a non-negative integer using a recursive approach.

    Parameters:
        n (int): The non-negative integer for which to calculate the factorial.

    Returns:
        int: The factorial of the integer.

    Raises:
        ValueError: If n is a negative number.
    """

    if n < 0:
        raise ValueError('The number must be a non-negative integer')
    if n in [0, 1]:
        return 1
    return n * iterative_factorial(n - 1)
