"""
This module provides functions for various geometric algorithms.
"""

from dataclasses import dataclass


@dataclass
class Point:
    """
    Represents a point in 2D space with coordinates (x,y). Default x=0, y=0.
    """
    x: int | float = 0
    y: int | float = 0


def distance_between_points(p1: Point, p2: Point) -> float:
    """
    Calculates the distance between two points in a 2-dimensional plane.

    Parameters:
        p1 (Point): The first point.
        p2 (Point): The second point.

    Returns:
        float: The distance between the two points.
    """

    return round(((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5, 2)


def are_points_collinear(point1: Point, point2: Point, point3: Point) -> bool:
    """
    Checks if three points are collinear.

    Parameters:
        point1 (Point): The first point.
        point2 (Point): The second point.
        point3 (Point): The third point.

    Returns:
        bool: True if the points are collinear, False otherwise.
    """

    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y
    x3, y3 = point3.x, point3.y
    slope_p1_p2 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope_p1_p3 = (y3 - y1) / (x3 - x1) if x3 - x1 != 0 else float('inf')
    return slope_p1_p2 == slope_p1_p3


def is_triangle_valid(a: int, b: int, c: int) -> bool:
    """
    Checks if given side lengths can form a valid triangle.

    Parameters:
        a (int): Length of side a.
        b (int): Length of side b.
        c (int): Length of side c.

    Returns:
        bool: True if the side lengths form a valid triangle, False otherwise.
    """

    if a + b > c and a + c > b and b + c > a:
        return True
    return False


def is_triangle_rectangular(s1: int, s2: int, s3: int) -> bool:
    """
    Checks if a triangle with given side lengths is a right-angled triangle.

    Parameters:
        s1 (int): Length of side 1.
        s2 (int): Length of side 2.
        s3 (int): Length of side 3.

    Returns:
        bool: True if the triangle is a right-angled triangle, False otherwise.
    """

    sides = [s1, s2, s3]
    sides.sort()
    return sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2
