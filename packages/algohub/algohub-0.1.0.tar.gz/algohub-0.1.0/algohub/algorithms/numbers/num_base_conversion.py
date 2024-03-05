"""
This module provides functions for working with conversion between number systems.
"""


def decimal_to_any(n: int, base: int = 2) -> str:
    """
    Converts a decimal number to its representation in the specified base.

    Parameters:
        n (int): The decimal number to convert.
        base (int): The base to convert the number to. Must be 2 or 8.

    Returns:
        str: The number's representation in the specified base.

    Raises:
        ValueError: If the specified base is not 2 or 8.
    """

    if base not in [2, 8]:
        raise ValueError('Uncorrect base. Must be 2 or 8')
    digits = []
    while n > 0:
        remainder = n % base
        digits.append(remainder)
        n //= base
    return ''.join(str(d) for d in digits)[::-1]


def any_to_decimal(num_str: str, base: int = 2) -> int:
    """
    Converts a number in the specified base to its decimal representation.

    Parameters:
        num_str (str): The number in the specified base.
        base (int): The base of the input number. Must be 2 or 8.

    Returns:
        int: The decimal representation of the input number.

    Raises:
        ValueError: If the specified base is not 2 or 8.
    """

    if base not in [2, 8]:
        raise ValueError('Uncorrect base. Must be 2 or 8')
    digits = []
    power = len(num_str) - 1
    for digit in num_str:
        if base == 2 and digit == '1':
            digits.append(2 ** power)
        elif base == 8:
            digits.append(int(digit) * (8 ** power))
        power -= 1
    return sum(digits)


def binary_to_hexadecimal(binary_num: str) -> str:
    """
    Converts a binary number to its hexadecimal representation.

    Parameters:
        binary_num (str): The binary number to convert.

    Returns:
        str: The hexadecimal representation of the input binary number.
    """

    while len(binary_num) % 4 != 0:
        binary_num = '0' + binary_num
    groups_of_four = [binary_num[i:i + 4] for i in range(0, len(binary_num), 4)]
    digits = []
    for group in groups_of_four:
        pow_ = len(group) - 1
        sum_ = 0
        for d in group:
            if d == '1':
                sum_ += (2 ** pow_)
            pow_ -= 1
        digits.append(sum_)
    decimal_to_hex = {
        10: 'A',
        11: 'B',
        12: 'C',
        13: 'D',
        14: 'E',
        15: 'F'
    }

    hexadecimal = [decimal_to_hex[d] if d >= 10 else str(d) for d in digits]
    while hexadecimal[0] == "0":
        hexadecimal.pop(0)
    return ''.join(hexadecimal)


def hexadecimal_to_binary(hex_num: str) -> str:
    """
    Converts a hexadecimal number to its binary representation.

    Parameters:
        hex_num (str): The hexadecimal number to convert.

    Returns:
        str: The binary representation of the input hexadecimal number.
    """

    hex_to_bin = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }
    return ''.join([hex_to_bin[d] for d in hex_num])


def decimal_to_hexadecimal(n: int) -> str:
    """
    Converts a decimal number to its hexadecimal representation.

    Parameters:
        n (int): The decimal number to convert.

    Returns:
        str: The hexadecimal representation of the input decimal number.
    """

    binary_representation = decimal_to_any(n, 2)
    return binary_to_hexadecimal(binary_representation)


def hexadecimal_to_decimal(num_str: str) -> int:
    """
    Converts a hexadecimal number to its decimal representation.

    Parameters:
        num_str (str): The hexadecimal number to convert.

    Returns:
        int: The decimal representation of the input hexadecimal number.
    """

    binary_representation = hexadecimal_to_binary(num_str)
    return any_to_decimal(binary_representation)


def binary_to_octal(binary: str) -> int:
    """
    Converts a binary number to its octal representation.

    Parameters:
        binary (str): The binary number to convert.

    Returns:
        int: The octal representation of the input binary number.
    """

    while len(binary) % 3 != 0:
        binary = '0' + binary
    groups_of_three = [binary[i:i + 3] for i in range(0, len(binary), 3)]
    digits = []
    for group in groups_of_three:
        pow_ = len(group) - 1
        sum_ = 0
        for d in group:
            if d == '1':
                sum_ += 2 ** pow_
            pow_ -= 1
        digits.append(sum_)

    while digits[0] == 0:
        digits.pop(0)
    return int(''.join([str(d) for d in digits]))


def octal_to_binary(octal: int) -> str:
    """
    Converts an octal number to its binary representation.

    Parameters:
        octal (int): The octal number to convert.

    Returns:
        str: The binary representation of the input octal number.
    """

    oct_to_bin = {
        '0': "000",
        '1': '001',
        '2': '010',
        '3': '011',
        '4': '100',
        '5': '101',
        '6': '110',
        '7': '111'
    }

    return ''.join([oct_to_bin[d] for d in str(octal)])


def octal_to_hexadecimal(octal: int) -> str:
    """
    Converts an octal number to its hexadecimal representation.

    Parameters:
        octal (int): The octal number to convert.

    Returns:
        str: The hexadecimal representation of the input octal number.
    """

    binary_str = octal_to_binary(octal)
    return binary_to_hexadecimal(binary_str)


def hexadecimal_to_octal(hexadecimal_str: str) -> int:
    """
    Converts a hexadecimal number to its octal representation.

    Parameters:
        hexadecimal_str (str): The hexadecimal number to convert.

    Returns:
        int: The octal representation of the input hexadecimal number.
    """

    binary_str = hexadecimal_to_binary(hexadecimal_str)
    return binary_to_octal(binary_str)
