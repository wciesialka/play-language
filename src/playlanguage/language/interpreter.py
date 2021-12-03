'''Module containing the Interpreter class,\
     which is responsible for running PlayLanguage programs.'''

import logging
from typing import List
import playlanguage.language.tokenizer as tokenizer
import playlanguage.language.tokens as tokens

class Interpreter:
    '''PlayLanguage Interpreter class.'''

    def __init__(self, raw_input: str):
        self.stack: List[int] = []
        reader = tokenizer.Tokenizer(self.stack)
        self.program: List[tokens.Token] = reader.read(raw_input)
        self.i: int = 0
        self.if_stack: List[bool] = []
        self.return_stack: List[int] = []
        self.save_register: int = None

    def get(self) -> tokens.Token:
        '''Get the current Token residing in the program at position "i"'''
        if self.i >= len(self.program):
            return None
        token = self.program[self.i]
        self.i = self.i + 1
        return token

    def interpret(self, /, condition: bool = True) -> bool:
        '''Run a program.
        :param condition: If we're in an if statement, was the condition true?
        :type condition: bool
        :returns: The unaltered condition.
        :rtype: bool'''

        while not (operation := self.get()) is None:

            if condition:
                logging.debug("Interpreting token %s", str(operation))
                if isinstance(operation, tokens.IfToken):
                    if_stack = self.interpret(condition=(self.stack[-1] != 0))
                    self.if_stack.append(if_stack)
                elif isinstance(operation, tokens.ElseToken):
                    self.interpret(condition=(not self.if_stack.pop()))
                elif isinstance(operation, tokens.ReturnToken):
                    self.return_stack.append(self.i-1)
                elif isinstance(operation, tokens.JumpToken):
                    self.i = self.return_stack.pop()
                elif isinstance(operation, tokens.ConditionalJumpToken):
                    temp = self.return_stack.pop()
                    if self.stack[-1] != 0:
                        self.i = temp
                elif isinstance(operation, tokens.SaveToken):
                    self.save_register = self.stack[-1]
                elif isinstance(operation, tokens.LoadToken):
                    self.stack.append(self.save_register)
                else:
                    value = operation()
                    if not value is None:
                        print(value, end="")
            if isinstance(operation, tokens.EndIfToken):
                logging.debug("Interpreting token %s", str(operation))
                return condition
