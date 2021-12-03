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
        self.return_stack = []
        self.save_register = None

    def get(self):
        if self.i >= len(self.program):
            return None
        token = self.program[self.i]
        self.i = self.i + 1
        return token

    def interpret(self,/,condition=True):

        while not (operation := self.get()) is None:

            if condition:
                logging.debug("Interpreting token %s",str(operation))
                if isinstance(operation,tokens.IfToken):
                    fi = self.interpret(condition = (self.stack[-1] != 0))
                    self.fi.append(fi)
                elif isinstance(operation,tokens.ElseToken):
                    self.interpret(condition = not self.fi.pop())
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
                        print(value,end="")
            if isinstance(operation, tokens.EndIfToken):
                logging.debug("Interpreting token %s",str(operation))
                return condition