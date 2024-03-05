# 📝 STRINGS ALGORITHMS 📝

## Overview

<font size="+1">
Package "strings" provides a collection of functions for working with strings. Algorithms for string analysis,
string manipulation and string sorting are implemented.


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
Once installed, you can import the strings package and utilize its functionalities in Python projects.
</font>

## Strings Analysis

<font size="+1">
This package contains a set of versatile functions for string analysis. These functions serve as 
useful tools for various text analysis tasks such as checking for anagrams or palindromes or detecting
duplicate elements in a list. <br>
Here's how you can use it:
<br>

```
from algohub.algorithms.strings import string_analysis
```

#### Checking for anagram

```
anagram = string_analysis.is_anagram("meat","team")
print(f'Result: {anagram}') # True
```

#### Checking for pangram

```
pangram = string_analysis.is_pangram("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
print(f'Result: {pangram}') # True
```

#### Checking for palindrome

```
palindrome = string_analysis.is_palindrome("KAYAK")
print(f'Palindrome: {palindrome}') # True
```  

#### Checking for potential palindrome

```
potential_palindrome = string_analyis.is_potential_palindrome("AABBCC")
print(f'Potential alindrome: {potential_palindrome}') # True
```

#### Checking for subsequence

```
text = "WORLD"
subsequence = "OD"
result = string_analyis.is_subsequence(text,subsequence)
print(f'Result : {result}') # True
```

#### Checking for substring

```
text = "WORLD"
substring = "ORL"
result = string_analyis.is_substring(text,substring)
print(f'Result : {result}') # True
```

#### Count of substring occurences

```
text = "PAPAYA"
substring = "PA"
result = string_analyis.count_substring_occurences(text,substring)
print(f'Count of substring occurences : {result}') # 2
```

#### Checking for duplicates

```
items = ["apple","banana","grapes","apple"]
result = string_analyis.contains_duplicates(items)
print(f'Items collection contains duplicates : {result}') # True
```

</font>

## Strings Manipulation

<font size="+1">
This package contains a set of versatile algorithms for string manipulation like string reverse,
string compression, custom join as well as methods for converting strings to lowercase and uppercase.<br>
Here's how you can use it:
<br>

```
from algohub.algorithms.strings import string_manipulation
```

#### Reversing a string

```
text = "HELLO WORLD"
reversed_text = string_manipulation.reverse(text)
print(f'Reversed text: {reversed_text}') # DLROW OLLEH
```

#### String compression

```
compressed_string = string_manipulation.compress("ABCABa")
print(f'Compression: {compressed_string}') # A2B2C1a1
```

#### Custom join

```
items = ["A","B","C","D","E"]
separator = "-"
text = string_manipulation.custom_join(items,separator)
print(f'Joined chars: {text}') # A-B-C-D-E
```  

#### Lowercase & Upperrcase

```
text = "MiXed CASED STRING2!"

lowercased = string_manipulation.lower(text)
print(f'Lowercased string: {lowercased}') # mixed cased string2!

uppercased = string_manipulation.upper(text)
print(f'Uppercased string: {uppercased}') # #MIXED CASED STRING2!                  
```

</font>

## Custom String Sorting

<font size="+1">
This package provides a flexible and customaizable solution for sorting
lists of strings based on a custom comparison criteria<br>
Here's how you can use it:
<br>

```
from algohub.algorithms.strings.custom_string_sorting import (
    sort_items,
    compare_chars_sum,
    compare_vowels_count
)
```

#### Sort items with compare_vowels_count and compare_chars_sum functions

```
words = ["BROTHER","COUSIN","DAD","CCC"]

sorted_items_by_vowels_count = sort_items(words, lambda text1, text2: compare_vowels_count(text1, text2))
print(f'sorted_items_by_vowels_count: {sorted_items_by_vowels_count}') # ["CCC","DAD","BROTHER","COUSIN"]

sorted_items_by_chars_sum = sort_items(words, lambda text1, text2: compare_chars_sum(text1, text2))
print(f'sorted_items_by_chars_sum: {sorted_items_by_chars_sum}') # ['DAD', 'CCC', 'COUSIN', 'BROTHER']
```

</font>






