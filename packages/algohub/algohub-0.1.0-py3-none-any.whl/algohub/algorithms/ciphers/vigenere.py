"""
This module provides functions for encoding and decoding text using the Vigenère cipher.
"""

from string import ascii_uppercase
from dataclasses import dataclass
from abc import ABC, abstractmethod


class _VigenereGenerator(ABC):
    """
    Abstract class for generating a Vigenere square.
    """

    @abstractmethod
    def generate_vigenere_square(self, n: int = 26) -> list[list[str]]:
        """
        Generates a Vigenere square of size 'n' (default is 26) as a list of lists,
        where each sublist represents a row of the Vigenere square.

        Parameters:
            n (int): Number of rows in the Vigenere square. Default is 26.

        Returns:
            list[list[str]]: A list of lists representing the Vigenere square.
        """

        pass


class _VigenereSquareGenerator(_VigenereGenerator):
    """
    A derived class of _VigenereGenerator class for generating a Vigenere square, which is a tabular
     arrangement of alphabets used in the Vigenere cipher for encryption and decryption.
    """

    def generate_vigenere_square(self, n: int = 26) -> list[list[str]]:
        """
        Generates a Vigenere square of size 'n' (default is 26) as a list of lists,
        where each sublist represents a row of the Vigenere square.

        Parameters:
            n (int): Number of rows in the Vigenere square. Default is 26.

        Returns:
            list[list[str]]: A list of lists representing the Vigenere square.
        """

        return [(list(ascii_uppercase[i:] + ascii_uppercase[:i])) for i in range(n)]


@dataclass
class VigenereCipher:
    """
    A class for Vigenere Cipher encryption and decryption.

    Attributes:
        key (str): A key used for encryption and decryption. It determines the row in the Vigenere
         square to use for each character.
        vigenere_generator (_VigenereGenerator): An instance of the Vigenere square generator.
    """

    key: str = 'KEY'
    vigenere_generator: _VigenereGenerator = _VigenereSquareGenerator()

    def encrypt(self, text: str) -> str:
        """
        Encrypts the given text using the Vigenere cipher and provided key.

        Parameters:
            text (str): Text to be encrypted.

        Returns:
            str: The encrypted text.
        """

        cleaned_text = [c for c in text if c.isalpha()]
        vigenere_square = self.vigenere_generator.generate_vigenere_square()
        chars = []
        # for i in range(len(cleaned_text)):
        for i, word in enumerate(cleaned_text):
            current_key_char = self.key[i % len(self.key)]
            row = ord(current_key_char) - ord('A')
            column = vigenere_square[0].index(word)
            encrypted_char = vigenere_square[row][column]
            chars.append(encrypted_char)
        return ''.join(chars)

    def decrypt(self, encrypted_text: str) -> str:
        """
         Decrypts the given encrypted text using the Vigenere cipher and provided key.

         Parameters:
             encrypted_text (str): Text to be decrypted.

         Returns:
             str: The decrypted text.
         """

        cleaned_text = [c for c in encrypted_text if c.isalpha()]
        vigenere_square = self.vigenere_generator.generate_vigenere_square()
        chars = []
        for i, word in enumerate(cleaned_text):
            current_key_char = self.key[i % len(self.key)]
            row = ord(current_key_char) - ord('A')
            column = vigenere_square[row].index(word)
            decrypted_char = vigenere_square[0][column]
            chars.append(decrypted_char)
        return ''.join(chars)
