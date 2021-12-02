from abc import ABCMeta, abstractmethod
import struct
from typing import List

MAX_BYTE_SIZE = 4

class TokenBuilder:
    '''Factory for creating tokens.'''

    def __init__(self, stack:List[int]):
        self._stack = stack

def add_builder(name:str):
    '''This decorator allows us to add build_x methods to TokenBuilder using a decorator\
        instead of rewriting similar method headers every time.
        :param name: Name of the class.
        :type name: str'''
    name = f"build_{name}"
    if name in TokenBuilder.__dict__.keys():
        raise ValueError(f"Attribute \"{name}\" already exists in TokenBuilder class.")

    def decorate(cls):
        def func(self,*args):
            return cls(self._stack,*args)

        setattr(TokenBuilder,name,func)

        
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
        packed = struct.pack(f"{len(self.stack)}i", *self.stack)
        return self.format(packed)

# Special Tokens
@add_builder("push")
class PushToken(Token):

    def __init__(self, stack:List[int], value:int):
        super().__init__(stack)
        
        if abs(value) > (1 << (MAX_BYTE_SIZE*8)):
            raise ValueError(f"Value of \"{value}\" exceeds max byte size of {MAX_BYTE_SIZE}.")
        self.value = value

    def func(self):
        self.stack.append(self.value)

@add_builder("pop")
class PopToken(Token):

    def func(self):
        return self.stack.pop()

@add_builder("peek")
class PeekToken(Token):

    def func(self):
        return self.stack[-1]

@add_builder("empty")
class EmptyToken(Token):

    def func(self):
        del self.stack[:]

@add_builder("non_op")
class NonOpToken(Token):

    def func(self):
        pass

@add_builder("chr")
class ChrToken(Token):

    def func(self):
        return chr(self.stack[-1])

# Unary Operation Tokens
@add_builder("not")
class NotToken(UnaryOperation):

    def operation(self, a: int):
        if a:
            return 0
        else:
            return 1

@add_builder("negate")
class NegateToken(UnaryOperation):

    def operation(self, a: int):
        return -a

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

@add_builder("and")
class AndToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a & b

@add_builder("or")
class OrToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a | b

@add_builder("left_shift")
class LeftShiftToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a << b

@add_builder("right_shift")
class RightShiftToken(BinaryOperation):

    def operation(self, a: int, b: int):
        return a >> b

# Formatter Tokens
@add_builder("tostring")
class ToStringToken(Formatter):
    def format(self, packed:bytes):
        unpacked = struct.unpack_from(f'{len(packed)}s', buffer=packed)[0]
        return unpacked.decode('utf-32')