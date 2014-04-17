'''
Created on 2014-04-17

@author: masegaloeh
'''

from abc import ABCMeta, abstractmethod
from math import pi, sqrt

class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return pi * self._radius * self._radius

    @property
    def perimeter(self):
        return 2 * pi * self._radius


class Rectangle(Shape):
    def __init__(self,height, width):
        self._height = height
        self._width = width

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def area(self):
        return self._width * self._height

    @property
    def perimeter(self):
        return 2 * (self._width + self._height)


class Triangle(Shape):
    def __init__(self, side_a, side_b, side_c):
        self._side_a = side_a
        self._side_b = side_b
        self._side_c = side_c

    #return list contain of three sides
    @property
    def getsides(self):
        return [self._side_a, self._side_b, self._side_c]

    # based on Heron Formula
    # http://en.wikipedia.org/wiki/Heron's_formula
    @property
    def area(self):
        s = (self._side_a + self._side_b + self._side_c)/2
        return sqrt(s * (s - self._side_a) * (s - self._side_b) * (s - self._side_c))

    @property
    def perimeter(self):
        return self._side_a + self._side_b + self._side_c
