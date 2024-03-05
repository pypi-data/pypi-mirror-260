"""
This module provides algorithms related to mathematical functions.
"""

from typing import Callable
import math


def bisection_root(func: Callable[[int | float], int | float],
                   a: int | float, b: int | float,
                   tolerance=1e-6,
                   max_iterations: int = 100) \
        -> int | float:
    """
    Finds a root of the given function within the interval [a, b]
     using the bisection method.

    Parameters:
        func (Callable[[int | float], int | float]): The function for
         which the root is to be found.
        a (int | float): The left endpoint of the interval.
        b (int | float): The right endpoint of the interval.
        tolerance (float, optional): The acceptable level of error in
         the root approximation. Defaults to 1e-6.
        max_iterations (int, optional): The maximum number of iterations. Defaults to 100.

    Returns:
        int | float: An approximation of the root within the specified tolerance.

    Raises:
        ValueError: If the function has the same sign at both endpoints (func(a) * func(b) > 0).
    """

    if func(a) * func(b) > 0:
        raise ValueError('The multiplication result must be a negative number')
    iteration = 0
    if a > b:
        a, b = b, a
    while (b - a) / 2 > tolerance and iteration < max_iterations:
        c = (a + b) / 2
        if func(c) == 0:
            return c
        if func(a) * func(c) < 0:
            b = c
        else:
            a = c
        iteration += 1
    return round((a + b) / 2, 3)


def quadratic_roots(a: int | float, b: int | float, c: int | float) -> \
        tuple[int | float | complex, int | float | complex]:
    """
    Calculates the roots of a quadratic equation ax**2 + bx + c = 0.

    Parameters:
        a (int | float): Coefficient of x^2.
        b (int | float): Coefficient of x.
        c (int | float): Constant term, function value when x = 0.

    Returns:
        tuple[int | float | complex, int | float | complex]: A tuple
         containing the roots of the quadratic equation.The roots
         can be integers, floats, or complex numbers.
    """

    if a == 0:
        raise ValueError(
            'Coefficient a must be a non-zero for a quadratic equation'
        )
    discriminant = b * b - 4 * a * c
    if discriminant > 0:
        root_1 = (-b - math.sqrt(discriminant)) / (2 * a)
        root_2 = (-b + math.sqrt(discriminant)) / (2 * a)
        return root_1, root_2
    if discriminant == 0:
        root = -b / (2 * a)
        return root, root

    real_part = -b / (2 * a)
    imaginary_part = math.sqrt(abs(discriminant)) / (2 * a)
    return real_part + imaginary_part * 1j, real_part - imaginary_part * 1j


def horner_evaluation(coefficients: list[int | float], x: int | float) -> int:
    """
    Evaluates a polynomial represented at the specified value of x.
    Used often to check whether x is the root of the equation or
    to calculate the value of polynpmial at x.

    Parameters:
        coefficients (list[int | float]): List of coefficients
         representing the polynomial.
        x (int | float): Value at which the polynomial is to be evaluated.

    Returns:
        int | float: Result of the polynomial evaluation at the given value.
    """

    result = 0
    for coefficient in coefficients:
        result = result * x + coefficient
    return result


def trapezoidal_integration(
        func: Callable[[int | float], int | float],
        a: int | float, b: int | float,
        n: int
) -> int | float:
    """
    Approximates the definite integral of a function using the trapezoidal
    rule. Evaluates area under the curve by dividing the total area into
    smaller trapzoids.

    Parameters:
        func (Callable[[int | float], int | float]): Function to be integrated.
        a (int | float): The lower limit of integration.
        b (int | float): The upper limit of integration.
        n (int): The number of trapezoids used to divide the area under
         the curve.

    Returns:
        float: The estimated value of the definite integral.
    """

    h = (b - a) / n
    integral_approximation = 0.5 * (func(a) + func(b))

    for i in range(1, n):
        x = a + i * h
        integral_approximation += func(x)
    return integral_approximation * h


def rectangular_integration(
        func: Callable[[int | float], int | float],
        a: int | float, b: int | float,
        n: int
) -> int | float:
    """
    Approximates the definite integral of a function using the rectangle rule.
    In other words - evaluates area under the curve by dividing the total area
    into smaller rectangles

    Parameters:
        func (Callable[[int | float], int | float]): Function to be integrate.
        a (int | float): The lower limit of integration.
        b (int | float): The upper limit of integration.
        n (int): The number of rectangles used to divide the area under the curve.

    Returns:
        float: The estimated value of the definite integral.
    """

    h = (b - a) / n
    integral_approximation = 0

    for i in range(n):
        x = a + (i + 0.5) * h
        rectangle_area = func(x) * h
        integral_approximation += rectangle_area
    return integral_approximation
