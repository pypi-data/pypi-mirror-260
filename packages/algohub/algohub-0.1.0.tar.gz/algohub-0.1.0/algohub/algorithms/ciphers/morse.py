"""
This module provides functions for encoding and decoding text using the Morse code.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class MorseCode:
    """
    A class for Morse Code encryption and decryption.

    Attributes:
        morse_code (ClassVar[dict[str,str]]): Morse code dictionary.
    """

    morse_code: ClassVar[dict[str, str]] = {'A': '.-', 'B': '-...',
                                            'C': '-.-.', 'D': '-..', 'E': '.',
                                            'F': '..-.', 'G': '--.', 'H': '....',
                                            'I': '..', 'J': '.---', 'K': '-.-',
                                            'L': '.-..', 'M': '--', 'N': '-.',
                                            'O': '---', 'P': '.--.', 'Q': '--.-',
                                            'R': '.-.', 'S': '...', 'T': '-',
                                            'U': '..-', 'V': '...-', 'W': '.--',
                                            'X': '-..-', 'Y': '-.--', 'Z': '--..',
                                            '1': '.----', '2': '..---', '3': '...--',
                                            '4': '....-', '5': '.....', '6': '-....',
                                            '7': '--...', '8': '---..', '9': '----.',
                                            '0': '-----', ',': '--..--', '.': '.-.-.-',
                                            '?': '..--..', '/': '-..-.', '-': '-....-',
                                            '(': '-.--.', ')': '-.--.-',
                                            }

    def encrypt(self, text: str) -> str:
        """
        Encrypts the given text using Morse code.

        Parameters:
            text (str): The text to be encrypted.

        Returns:
            str: The encrypted text represented in Morse code.

        Raises:
            ValueError: If a character in the input is not in Morse code dictionary.
        """

        chars = []
        for c in text:
            chars.append(self.morse_code[c.upper() if c.isalpha() else c])
        return '|'.join(chars)

    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypts the given Morse code to obtain the original text.

        Parameters:
            encrypted_text (str): The encrypted text in Morse code.

        Returns:
            str: The decrypted original text.

        Raises:
            ValueError: If a character in the text is not present
             in the reversed Morse code dictionary.
        """

        encoded_chars = encrypted_text.split("|")
        reversed_morse_code = {value: key for key, value in self.morse_code.items()}
        chars = []
        for c in encoded_chars:
            chars.append(reversed_morse_code[c if c.isalpha() else c])
        return ''.join(chars)
