import playlanguage.language.tokens as tokens
import logging
from typing import Callable, List, Dict

class Tokenizer:

    def __init__(self, stack:List[int]):
        self.__builder = tokens.TokenBuilder(stack)
        self.__number = 0
        self.__reading_number = False

    def __build_push(self):
        logging.info("Building push token %i",self.__number)
        token = self.__builder.build_push(self.__number)
        self.__number = 0
        self.__reading_number = False
        return token

    def read(self, string:str):
        logging.info("Tokenizing program.")

        symbols:Dict[str, Callable[[],]] = {
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
            "=": self.__builder.build_equality
        }

        tokens:List = []

        escape = False
        stringing = False
        comment = False

        for char in string:

            if comment:
                if char == "#":
                    comment = False
            else:
                if stringing:
                    if escape:
                        tokens.append(self.__builder.build_push(ord(char)))
                        escape = False
                    else:
                        if char == "\\":
                            escape = True
                        elif char == "\"":
                            stringing = False
                        else:
                            tokens.append(self.__builder.build_push(ord(char)))
                else:
                    logging.debug("Reading character \"%s\"",char)
                    # Whitespace
                    if char.isspace():
                        pass
                    # String
                    elif char == '"':
                        stringing = True
                    # Comment
                    elif char == '#':
                        comment = True
                    # Digit
                    elif char.isdigit():
                        self.__reading_number = True
                        self.__number *= 10
                        self.__number += int(char)
                    # Operation
                    elif char in symbols.keys():
                        # If we're done reading a number
                        if self.__reading_number:
                            tokens.append(self.__build_push())
                        logging.info("Building token %s",char)
                        tokens.append(symbols[char]())
                    # Invalid
                    else:
                        raise NotImplementedError(f"Token \"{char}\" undefined.")

        # if last line was a push...
        if self.__reading_number:
            tokens.append(self.__build_push())
            
        return tokens

