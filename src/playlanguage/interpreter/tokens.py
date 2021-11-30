from abc import abstractmethod

import abc
from typing import List

class TokenBuilder:

    def __init__(self, stack:List[int]):
        self.__stack = stack

    def build_push(self, value:int):
        return Push(self.__stack, value)

    def build_pop(self):
        return Pop(self.__stack)

    def build_add(self):
        return Add(self.__stack)

    def build_subtract(self):
        return Subtract(self.__stack)

class Token:

    __metaclass__ = abc.ABCMeta

    def __init__(self, stack:List[int]):
        self.stack = stack

    @abc.abstractmethod
    def func(self):
        return

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

class Push(Token):

    def __init__(self, stack:List[int], value:int):
        super().__init__(stack)
        self.value = value

    def func(self):
        self.stack.append(self.value)

class Pop(Token):

    def func(self):
        return self.stack.pop()

class BinaryOperation(Token):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def operation(self, a:int, b:int):
        return

    def func(self):
        b = self.stack.pop()
        a = self.stack.pop()
        self.stack.append(self.operation(a, b))

class Add(BinaryOperation):

    def operation(self, a: int, b: int):
        return a + b

class Subtract(BinaryOperation):

    def operation(self, a: int, b: int):
        return a - b