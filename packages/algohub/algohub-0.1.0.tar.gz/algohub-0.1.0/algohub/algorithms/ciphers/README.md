# 🔐 CIPHERS ALGORITHMS 🔐
## Overview
<font size="+1">
Welcome to the "ciphers" package of the "algorithms" library. This package
provides implementations of various classical ciphers, including 
Vigenère cipher, Caesar cipher and Morse code.
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
Once installed, you can import the ciphers package and utilize its functionalities in Python. 
</font>

## Vigenère Cipher
<font size="+1">
The Vigenère cipher uses a 26×26 table with A to Z as the row heading and column heading. This table
is usually referred to as the Vigenère Square.The first row of this table has the 26
English letters. Starting with the second row, each row has the letters 
shifted to the left one position in a cyclic way. For example, when B is shifted to 
the first position on the second row, the letter A moves to the end.<br>
Here's how you can use it:
<br>
  
```
from algohub.algorithms.ciphers import vigenere
```

```
# Creating an instance of Vigenère square
key = "CAT" 
vigenere_square = VigenereCipher(key)
```

```
# Encrypting a text
plaintext = "HOME"
encrypted_text = vigenere_square.encrypt(plaintext)
print(f'Encrypted: {encrypted_text}')              #JOFG
```
```
# Decrypting a text
decrypted_text = vigenere_square.decrypt(encrypted_text)
print(f'Decrypted: {decrypted_text}')             # HOME
```

</font>

## Caesar Cipher 
<font size="+1">
The Caesar cipher is one of the simplest and most widely 
known encryption techniques. It shifts the letters of the alphabet by a certain 
number of places down or up the alphabet.<br>
Here's how you can use it:

```
from algohub.algorithms.ciphers import caesar
```

```
# Creating an instance of Caesar cipher
shift = 2
caesar_cipher = CaesarCipher(shift)
```
```
# Encrypting a text
plaintext = 'ABCD'
encrypted_text = caesar_cipher.encrypt(plaintext)
print(f'Encrypted: {encrypted_text}')           # CDEF
```
```
# Decrypting a text
decrypted_text = caesar_cipher.decrypt(encrypted_text)
print(f'Decrypted: {decrypted_text}')           # ABCD
```
</font>

## Morse Code
<font size="+1">

Morse code is a method used in telecommunication to encode text characters 
as sequences of two different signal durations, called dots and dashes.<br>
Here is how you can use it:<br>

```
from algohub.algorithms.ciphers import morse
```
```
Creating an instance of Morse code
morse_code = MorseCode()
```
```
# Encrypting a text
plaintext = 'HOUSE'
encrypted_text = morse_code.encrypt(plaintext)
print(f'Encrypted: {encrypted_text}')           #  ....|---|..-|...|.
```
```
# Decrypting a text
decrypted_text = morse_code.decrypt(encrypted_text)
print(f'Decrypted: {decrypted_text}')           # HOUSE
```
</font>
