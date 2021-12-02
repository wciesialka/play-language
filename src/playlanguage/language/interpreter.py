import playlanguage.language.tokenizer as tokenizer
import playlanguage.language.tokens as tokens
import logging

class Interpreter:

    def __init__(self, raw_input:str):
        self.stack = []
        reader = tokenizer.Tokenizer(self.stack)
        self.program = reader.read(raw_input)
        self.i = 0
        self.fi = []

    def get(self):
        if self.i >= len(self.program):
            return None
        token = self.program[self.i]
        self.i = self.i + 1
        return token

    def interpret(self,/,condition=True):

        while not (operation := self.get()) is None:
            if condition:
                if isinstance(operation,tokens.IfToken):
                    fi = self.interpret(condition = (self.stack[-1] != 0))
                    self.fi.append(fi)
                elif isinstance(operation,tokens.ElseToken):
                    self.interpret(condition = not self.fi.pop())
                else:
                    value = operation()
                    if not value is None:
                        print(value,end="")
            if isinstance(operation, tokens.EndIfToken):
                return condition