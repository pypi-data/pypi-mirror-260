"""
This module provides functions for encoding and decoding text using the Caesar cipher.
"""

from dataclasses import dataclass
from typing import ClassVar
from string import ascii_uppercase


@dataclass
class CaesarCipher:
    """
    A class for implementing the Caesar cipher, a simple substitution cipher
    where each letter in the plaintext is shifted a certain number of places
    down or up the alphabet.

    Attributes:
        sequence:str
         A sequence of characters representing the alphabet. Default is the
         ASCII uppercase characters.
        shift: int
         The number of positions each letter is shifted. Default is 3.
    """

    sequence: ClassVar[str] = ascii_uppercase
    shift: int = 3

    def _encrypt_char(self, char: str) -> str:
        """
        Encrypts a single character using the Caesar cipher.

        Parameters:
            char (str): The character to be encrypted.

        Returns:
            str: The encrypted character.
        """

        if char.isalpha() and char.isupper():
            return self.sequence[(self.sequence.index(char) + self.shift) % 26]
        return char

    def _decrypt_char(self, char: str) -> str:
        """
        Decrypts a single character using the Caesar cipher.

        Parameters:
            char (str): The character to be decrypted.

        Returns:
            str: The decrypted character.
        """

        if char.isalpha() and char.isupper():
            return self.sequence[(self.sequence.index(char) - self.shift) % 26]
        return char

    def encrypt(self, text: str) -> str:
        """
        Encrypts a given text using the Caesar cipher.

        Parameters:
            text (str): The text to be encrypted.

        Returns:
            str: The encrypted text.
        """

        return ''.join([self._encrypt_char(c) for c in text])

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypts a given encrypted text using the Caesar cipher.

        Parameters:
            encrypted_text (str): The encrypted text to be decrypted.

        Returns:
            str: The decrypted text.
        """

        return ''.join([self._decrypt_char(c) for c in encrypted_text])
