'''Module containing the TokenBuilder class and all Tokens.'''

from abc import ABCMeta, abstractmethod
import struct
from typing import List

MAX_BYTE_SIZE: int = 4

class TokenBuilder:
    '''Factory for creating tokens.'''

    def __init__(self, stack: List[int]):
        self._stack = stack

def add_builder(name: str):
    '''This decorator allows us to add build_x methods to TokenBuilder using a decorator\
        instead of rewriting similar method headers every time.
        :param name: Name of the class.
        :type name: str'''
    name = f"build_{name}"
    if name in TokenBuilder.__dict__.keys():
        raise ValueError(f"Attribute \"{name}\" already exists in TokenBuilder class.")

    def decorate(cls):
        def func(self, *args):
            return cls(self._stack, *args)

        setattr(TokenBuilder, name, func)
        return cls

    return decorate

class Token:
    '''Base token abstract class. Takes in a stack and perform actions on that stack.'''

    __metaclass__ = ABCMeta

    def __init__(self, stack: List[int]):
        self.stack = stack

    @abstractmethod
    def func(self):
        '''Perform the function of the Token.'''
        return

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def __str__(self):
        return self.__class__.__name__

class BinaryOperation(Token):
    '''Base Binary Operation abstract class.'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def operation(self, a: int, b: int):
        '''Perform the binary operation.'''
        return

    def func(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(self.operation(a, b))

class UnaryOperation(Token):
    '''Base Unary Operation abstract class.'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def operation(self, a: int):
        '''Perform the unary operation.'''
        return

    def func(self):
        a = self.stack.pop()
        self.stack.append(self.operation(a))

class Formatter(Token):
    '''Base Formatter abstract class.'''
    __metaclass__ = ABCMeta

    @abstractmethod
    def format(self, packed: bytes):
        '''Format the packed bytes into something new.'''
        return

    def func(self):
        #size = getsizeof(self.stack)
        packed = struct.pack(f"{len(self.stack)}i", *self.stack)
        return self.format(packed)

# Special Tokens
@add_builder("push")
class PushToken(Token):
    '''Push a value onto the stack.'''
    def __init__(self, stack: List[int], value: int):
        super().__init__(stack)

        if abs(value) > (1 << (MAX_BYTE_SIZE*8)):
            raise ValueError(f"Value of \"{value}\" exceeds max byte size of {MAX_BYTE_SIZE}.")
        self.value = value

    def func(self):
        '''Push our value.'''
        self.stack.append(self.value)

    def __str__(self):
        return f"PushToken({self.value})"

@add_builder("pop")
class PopToken(Token):
    '''Pop from the top of the stack and return it.'''
    def func(self):
        return self.stack.pop()

@add_builder("peek")
class PeekToken(Token):
    '''Return what's on top of the stack.'''
    def func(self):
        return self.stack[-1]

@add_builder("empty")
class EmptyToken(Token):
    '''Empty the stack.'''
    def func(self):
        del self.stack[:]

@add_builder("non_op")
class NonOpToken(Token):
    '''Do nothing.'''
    def func(self):
        pass

@add_builder("chr")
class ChrToken(Token):
    '''Peek at the top of the stack, but as a character.'''
    def func(self):
        return chr(self.stack[-1])

@add_builder("copy")
class CopyToken(Token):
    '''Push the value at the top of the stack onto the stack.'''
    def func(self):
        self.stack.append(self.stack[-1])

@add_builder("if")
class IfToken(Token):
    '''If token.'''
    def func(self):
        pass

@add_builder("endif")
class EndIfToken(Token):
    '''End if token.'''
    def func(self):
        pass

@add_builder("else")
class ElseToken(Token):
    '''Else token.'''
    def func(self):
        pass

@add_builder("return")
class ReturnToken(Token):
    '''Set a return point.'''
    def func(self):
        pass

@add_builder("jump")
class JumpToken(Token):
    '''Jump to return point.'''
    def func(self):
        pass

@add_builder("conditional_jump")
class ConditionalJumpToken(Token):
    '''Conditional jump to return point.'''
    def func(self):
        pass

@add_builder("save")
class SaveToken(Token):
    '''Save to register.'''
    def func(self):
        pass


@add_builder("load")
class LoadToken(Token):
    '''Load from register.'''
    def func(self):
        pass

# Unary Operation Tokens
@add_builder("not")
class NotToken(UnaryOperation):
    '''If true, push 0, if false, push 1'''
    def operation(self, a: int):
        if a:
            return 0
        return 1

@add_builder("negate")
class NegateToken(UnaryOperation):
    '''Push the negative of the value on top of the stack.'''

    def operation(self, a: int):
        return -a

# Binary Operation Tokens

@add_builder("add")
class AddToken(BinaryOperation):
    '''Add the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a + b

@add_builder("subtract")
class SubtractToken(BinaryOperation):
    '''Subtract the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a - b

@add_builder("multiply")
class MultiplyToken(BinaryOperation):
    '''Multiply the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a * b

@add_builder("divide")
class DivideToken(BinaryOperation):
    '''Divide the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a//b

@add_builder("modulo")
class ModuloToken(BinaryOperation):
    '''Modulo the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a % b

@add_builder("band")
class BandToken(BinaryOperation):
    '''Bitwise and the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a & b

@add_builder("bor")
class BorToken(BinaryOperation):
    '''Bitwise or the two numbers on top of the stack.'''

    def operation(self, a: int, b: int):
        return a | b

@add_builder("equality")
class EqualityToken(BinaryOperation):
    '''If the two numbers on top of the stack are equal, push 1. 0 otherwise.'''

    def operation(self, a: int, b: int):
        if a == b:
            return 1
        return 0

@add_builder("greater_than")
class GreaterThanToken(BinaryOperation):
    '''Pop two numbers from the stack. If the first is greater than the \
        second, push 1. Push 0 otherwise.'''

    def operation(self, a: int, b: int):
        if a > b:
            return 1
        return 0

@add_builder("less_than")
class LessThanToken(BinaryOperation):
    '''Pop two numbers from the stack. If the first is less than the \
        second, push 1. Push 0 otherwise.'''


    def operation(self, a: int, b: int):
        if a < b:
            return 1
        return 0

# Formatter Tokens
@add_builder("tostring")
class ToStringToken(Formatter):
    '''Turn the stack into a string.'''

    def format(self, packed: bytes):
        unpacked = struct.unpack_from(f'{len(packed)}s', buffer=packed)[0]
        return unpacked.decode('utf-32')
