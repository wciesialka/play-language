from abc import ABCMeta, abstractmethod
import struct
from typing import List

class TokenBuilder:
    '''Factory for creating tokens.'''
    def __init__(self, stack:List[int]):
        self.stack = stack

def add_builder(name:str):
    '''This decorator allows us to add build_x methods to TokenBuilder using a decorator\
        instead of rewriting similar method headers every time.
        :param name: Name of the class.
        :type name: str'''
    def decorate(cls):
        def func(self,*args):
            return cls(self.stack,*args)

        setattr(TokenBuilder,f"build_{name}",func)
    return decorate

class Token:
    '''Base token abstract class. Takes in a stack and perform actions on that stack.'''

    __metaclass__ = ABCMeta

    def __init__(self, stack:List[int]):
        self.stack = stack

    @abstractmethod
    def func(self):
        return

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class BinaryOperation(Token):

    __metaclass__ = ABCMeta

    @abstractmethod
    def operation(self, a:int, b:int):
        return

    def func(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(self.operation(a, b))

class UnaryOperation(Token):

    __metaclass__ = ABCMeta

    @abstractmethod
    def operation(self, a:int):
        return
    
    def func(self):
        a = self.stack.pop()
        self.stack.append(self.operation(a))

class Formatter(Token):

    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, packed:bytes):
        return

    def func(self):
        #size = getsizeof(self.stack)
        packed = struct.pack(f"{len(self.stack)}l", *self.stack)
        return self.format(packed)

# Special Tokens
@add_builder("push")
class Push(Token):

    def __init__(self, stack:List[int], value:int):
        super().__init__(stack)
        self.value = value

    def func(self):
        self.stack.append(self.value)

@add_builder("pop")
class Pop(Token):

    def func(self):
        return self.stack.pop()

# Unary Operation Tokens


# Binary Operation Tokens
@add_builder("add")
class AddToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a + b

@add_builder("subtract")
class SubtractToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a - b

@add_builder("multiply")
class MultiplyToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a * b

@add_builder("divide")
class DivideToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a//b

# Formatter Tokens
@add_builder("tostring")
class ToStringToken(Formatter):
    def format(self, packed:bytes):
        unpacked = struct.unpack_from(f'{len(packed)}s', buffer=packed)[0]
        return unpacked.decode('utf-8')

@add_builder("tofloat")
class ToFloatToken(Formatter):
    def format(self, packed:bytes):
        unpacked = struct.unpack_from(f'{len(packed)}f', buffer=packed)[0]
        return unpacked