'''Module containing the Tokenizer class, which\
     reads programs and turns them into tokens that can be run.'''

import logging
from typing import Callable, List, Dict
import playlanguage.language.tokens as tokens

class Tokenizer:

    '''Class responsible for reading strings and turning them into a list of executable tokens.'''

    def __init__(self, stack: List[int]):
        self.__builder: tokens.TokenBuilder = tokens.TokenBuilder(stack)
        self.__number: int = 0
        self.__reading_number: bool = False

    def __build_push(self) -> tokens.PushToken:
        '''Build a Push Token using the internal "number" value.'''

        logging.info("Building push token %i", self.__number)
        token = self.__builder.build_push(self.__number)
        self.__number = 0
        self.__reading_number = False
        return token

    def read(self, string: str) -> List[tokens.Token]:
        '''Read source code and return a list of executable tokens.
        :param string: The program to read.
        :type string: str
        :returns: A list of executable tokens.
        :rtype: tokens.Token'''

        logging.info("Tokenizing program.")

        # This is our dictionary of symbols and what build function
        # should be called when that symbol is encountered.
        symbols: Dict[str, Callable[[], tokens.Token]] = {
            "+": self.__builder.build_add,
            "-": self.__builder.build_subtract,
            "*": self.__builder.build_multiply,
            "/": self.__builder.build_divide,
            ".": self.__builder.build_pop,
            ",": self.__builder.build_non_op,
            ":": self.__builder.build_peek,
            "e": self.__builder.build_empty,
            "c": self.__builder.build_chr,
            "!": self.__builder.build_not,
            "~": self.__builder.build_negate,
            "&": self.__builder.build_and,
            "|": self.__builder.build_or,
            "s": self.__builder.build_tostring,
            "?": self.__builder.build_copy,
            "(": self.__builder.build_if,
            ")": self.__builder.build_endif,
            "=": self.__builder.build_equality,
            ">": self.__builder.build_greater_than,
            "<": self.__builder.build_less_than,
            "%": self.__builder.build_modulo,
            "{": self.__builder.build_else,
            "r": self.__builder.build_return,
            "j": self.__builder.build_jump,
            "q": self.__builder.build_conditional_jump,
            "$": self.__builder.build_save,
            "^": self.__builder.build_load
        }

        token_list: List[tokens.Token] = []

        escape: bool = False
        stringing: bool = False
        comment: bool = False

        for char in string:

            if comment:
                if char == "#":
                    comment = False
            else:
                if stringing:
                    if escape:
                        token_list.append(self.__builder.build_push(ord(char)))
                        escape = False
                    else:
                        if char == "\\":
                            escape = True
                        elif char == "\"":
                            stringing = False
                        else:
                            token_list.append(self.__builder.build_push(ord(char)))
                else:
                    # Whitespace
                    if char.isspace():
                        if self.__reading_number:
                            token_list.append(self.__build_push())
                    # String
                    elif char == '"':
                        stringing = True
                    # Comment
                    elif char == '#':
                        comment = True
                    # Digit
                    elif char.isdigit():
                        logging.debug("Reading digit \"%s\"", char)
                        self.__reading_number = True
                        self.__number *= 10
                        self.__number += int(char)
                    # Operation
                    elif char in symbols.keys():
                        logging.debug("Reading character \"%s\"", char)
                        # If we're done reading a number
                        if self.__reading_number:
                            token_list.append(self.__build_push())
                        logging.info("Building token %s", char)
                        token_list.append(symbols[char]())
                    # Invalid
                    else:
                        raise NotImplementedError(f"Token \"{char}\" undefined.")

        # if last line was a push...
        if self.__reading_number:
            token_list.append(self.__build_push())

        return token_list
