# 🔢 NUMBERS ALGORITHMS 🔢

## Overview

<font size="+1">
Welcome to the "numbers" package of the "algorithms" library. This package
provides functionalities for dealing with numbers, including digit operations,
number base conversion and prime numbers. 
</font>

## Installation

<font size="+1">
To install the "algorithms" library and access this package, you can use pip:<br>
<br>

```
pip install algohub
```

</font>

## Usage

<font size="+1">
Once installed, you can import the numbers package and utilize its functionalities in Python. 
</font>

## Digits 🧮

<font size="+1">
Digits module provides functionalities for digits operations, like
getting the digit at the specific position, summing digits of the number
and moving zeroes at the end of the list.<br>
Here is how you can use it:
<br>

```
from algohub.algorithms.numbers import digits
```

#### Digit at specified position

```
number = 532

first_digit = digits.get_digit(number, 0)               
second_digit = digits.get_digit(number, 1)              
third_digit = digits.get_digit(number, 2)               
out_of_range_position = digits.get_digit(number, 5)     

print(f'Digit at first position: {first_digit}')                    # 2
print(f'Digit at second position: {second_digit}')                  # 3
print(f'Digit at third position: {third_digit}')                    # 5
print(f'Digit at out of range position: {out_of_range_position}')   # 0
```

#### Digits sum

```
number = 128
number_2 = -159

digits_sum = digits.sum_digits(number)     
digits_sum_2 = digits.sum_digits(number_2) 

print(f'Digits sum of number: {digits_sum}')      # 11
print(f'Digits sum of number_2: {digits_sum_2}')  # 15
```

#### Moving zeroes

```
numbers = [0, 1, 0, 2, 4, 0, 5]
numbers_with_zeroes_at_the_end = digits.move_zeroes(numbers) 

print(f'Numbers with zeroes at the end: {numbers_with_zeroes_at_the_end}') #  [1, 2, 4, 5, 0, 0, 0] 
```  

</font>

## Divisors 🧮

<font size="+1">
Digits module provides functionalities for calculating divisors of integers
and their properties. It includies functions for counting divisors, finding common
divisors between two numbers, and summing divisors of a given number.<br>
Here's how you can use it:<br>

```
from algohub.algorithms.numbers import divisors
```

#### Count divisors

```
number = 18

divisors_count = divisors.count_divisors(number)    
print(f'Divisors count of {number}: {divisors_count}')    # 6
```

#### Count common divisors

```
number_1 = 24
number_2 = 4

common_divisors_count = divisors.count_common_divisors(number_1, number_2)
print(f'Common divisors count of {number_1} and {number_2}: {common_divisors_count}')  # 3
```

#### Sum divisors

```
number = 10

divisors_sum = divisors.sum_divisors(number)
print(f'Divisors sum of {number}: {divisors_sum}')  # 18
```

</font>

## Primes 🧮

<font size="+1">
The primes module provies functionalities for determining prime numbers
and prime factors. It includes methods for checking if a number is prime
using Erastothenes Sieve or a basic algorithm, as well as finding prime
factors of a given number.<br>
Here's how you can use it:
<br>

```
from algohub.algorithms.numbers.primes import (
    ErastothenesSieve,
    is_prime_basic,
    get_prime_factors,
    is_perfect_number
)
```

#### Erastothenes sieve

```
# Creating an instance of Erastothenes sieve
sieve = ErastothenesSieve(100)
number_1 = 41
prime_number = sieve.is_prime(number_1)
number_2 = 18
not_prime_number =  sieve.is_prime(number_2)

print(f'Prime number {number_1}: {prime_number}')               # True
print(f'Not a prime number {number_2}: {not_prime_number}')     # False
```

#### Prime checker - basic function

```
number_1 = 13
number_2 = 4

prime_number = is_prime_basic(number_1)
not_prime_number = is_prime_basic(number_2)

print(f'Prime number {number_1}: {prime_number} ')            # True
print(f'Not a prime number {number_2}: {not_prime_number} ')  # False
```

#### Getting prime factors

```
number = 18
prime_factors = get_prime_factors(number)

print(f'Prime factors of {number}: {prime_factors}')  # [2,3,3]
```

#### Checking for perfect number

```
number = 6
perfect_number = is_perfect_number(number)

print(f'Perfect number {number}: {perfect_number}')  # True
```

</font>

## Number base conversion 🧮

<font size="+1">

Number base conversion 🧮
The number base conversion module offers functions to convert numbers between
different bases, including decimal, binary, octal, and hexadecimal.<br>
Here's how you can use it:
<br>

```
from algohub.algorithms.numbers.num_base_conversion import (
    decimal_to_any,
    any_to_decimal,
    decimal_to_hexadecimal,
    hexadecimal_to_decimal,
    binary_to_hexadecimal,
    hexadecimal_to_binary,
    binary_to_octal,
    octal_to_binary,
    octal_to_hexadecimal,
    hexadecimal_to_octal
)
```

#### Decimal & binary conversion

```
decimal_number = 10
binary_number = decimal_to_any(decimal_number, 2)

print(f'Binary representation of {decimal_number}: {binary_number}')  # 1010

binary_number = "1111" 
decimal_number = any_to_decimal(binary_number, 2)

print(f'Decimal representation of {binary_number}: {decimal_number}')  # 15
```

#### Decimal & octal conversion

```
decimal_number = 10
octal_number = decimal_to_any(decimal_number, 8)
print(f'Octal representation of {decimal_number}: {octal_number}')      # 12

octal_number = "144"
decimal_number = any_to_decimal(octal_number, 8)

print(f'Decimal representation of {octal_number}: {decimal_number}')    # 100
```

#### Decimal & hexadecimal conversion

```
decimal_number = 43
hex_number = decimal_to_hexadecimal(decimal_number)

print(f'Hexadecimal representation of {decimal_number}: {hex_number}')      # "2B"

hex_number = "1AB"
decimal_number = hexadecimal_to_decimal(hex_number)

print(f'Decimal representation of {hex_number}: {decimal_number}')          # 427
```

#### Binary & hexadecimal conversion

```
binary_number = "11011"
hex_number = binary_to_hexadecimal(binary_number)   

print(f'Hexadecimal representation of {binary_number}: {hex_number}')       # 1B

hex_number = "A2"
binary_number = hexadecimal_to_binary(hex_number)

print(f'Binary representation of {hex_number}: {binary_number}')            # 10100010
```

#### Binary & octal conversion

```
binary_number = "10110"
octal_number = binary_to_octal(binary_number)

print(f'Octal representation of {binary_number}: {octal_number}')        # 26

octal_number = 127
binary_number = octal_to_binary(octal_number)

print(f'Binary representation of {octal_number}: {binary_number}')       # 001010111
```

#### Octal & hexadecimal conversion

```
octal_number = 50
hex_number =  octal_to_hexadecimal(octal_number)

print(f'Hexadecimal representation of {octal_number}: {hex_number}')    # 28

hex_number = "A12"
octal_number = hexadecimal_to_octal(hex_number)

print(f'Octal representation of {hex_number}: {octal_number}')          # 5022
```

</font>

