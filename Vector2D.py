# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 04:03:09 2019

@author: Chris Mitchell

TO DO
    . Add docstrings for class and methods
    . Broaden doctest for all functions
    
"""

from math import sqrt, acos, atan, pi
from SimpleVector import SimpleVector

class Vector2D(SimpleVector):

    def __init__(self, head, tail = []):
        
        if isinstance(head, __class__):
            if head._dim != 2:
                raise Exception("Vector2D can only be initialized with a two-dimensional vector.")
            else:
                self._head = head._head.copy()
                self._tail = head._tail.copy()
                self._dim = head._dim
                self._dtype = head._dtype
                self._origin = head._origin.copy()
                self._component = head._component.copy()
                return
        else:
            try:
                _ = list(head)
            except TypeError:
                raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
            except:
                raise Exception("Unknown error in class constructor.")
            if len(list(head)) != 2:
                raise Exception("Vector2D can only be initialized with a two-dimensional list.")
                
        super().__init__(head, tail)

    def _checkTypeCompatability(self, other):
        """
        A type check to make sure that operations between vectors are specified
        using the SimpleVector class or Vector2D clas and that they share both
        dimension.
        """
        if not isinstance(other, __class__):
            raise TypeError("Both arguments must be of the Vector2D class.")
        if other.dim != 2:
            raise Exception("Vectors are of unequal dimension.")

    def angle(self, other, units = "rad"):
        self._checkTypeCompatability(other)
        if units not in ["rad", "radians", "deg", "degrees"]:
            raise Exception('Units must be "rad" or "deg" for radians or degrees.')
        else:
            units = units[:3]
        cosineTheta = self.dot(other) / (self.norm() * other.norm())
        result = acos(cosineTheta)
        if units == "deg":
            result = result * 180 / pi
        return result
    
    def asLine(self, symbolX = 'x', symbolY = 'y', symbolT = 't'):
        if self._tail == []:
            tempTail = [0, 0]
        else:
            tempTail = self._tail
        return '\u27e8' + symbolX + ', ' + symbolY + '\u27e9 = (' + str(tempTail)[1:-1] + ') + ' + symbolT + '\u27e8' + str(self._head)[1:-1] + '\u27e9'
        
    def asCartesianLine(self, symbolX = 'x', symbolY = 'y'):
        m = self.y / self.x
        if self._tail == []:
            bX = 0
            bY = 0
        else:
            bX = self._tail[0]
            bY = self._tail[1]
        b = bY - m * bX
        if m.is_integer():
            m = int(m)
        if b.is_integer():
            b = int(b)
        if b < 0:
            addSym = '-'
        else:
            addSym = '+'
        if m == 0:
            return symbolY + ' = ' + str(b)
        if m == 1:
            return symbolY + ' = x ' + addSym + ' ' + str(abs(b))
        else:
            return symbolY + ' = ' + str(m) + symbolX + ' ' + addSym + ' ' + str(abs(b))
        
    def asParametricLine(self, symbolT = 't'):
        if self._tail == []:
            tempTail = [0, 0]
        else:
            tempTail = self._tail
        if self.x < 0:
            addSymX = '-'
        else:
            addSymX = '+'
        if self.y < 0:
            addSymY = '-'
        else:
            addSymY = '+'
        return '\u27e8' + str(self._tail[0]) + ' ' + addSymX + ' ' + str(self.x) + symbolT + ', ' + str(self._tail[1]) + ' ' + addSymY + ' ' + str(self.y) + symbolT + '\u27e9'

    def toPolar(self, units = "rad"):
        """
        toPolar will return will return the vector in [r, theta] form,
        r being the length of the vector and theta being its angle from
        the positive x-axis. Both r and theta will always be positive and
        theta will be 0 <= theta < 2 * pi or 0 <= theta < 360 depending on
        selected units. If the tail is anywhere but the origin, the origin
        will be reset to (0, 0). If the vector is the zero vector, (0, 0)
        will be returned.
        
        [r, theta] will be returned as a list, not as a new vector.
        """
        if self[0] == 0 and self[1] == 0:
            return [0, 0]
        if units not in ["rad", "radians", "deg", "degrees"]:
            raise Exception('Units must be "rad" or "deg" for radians or degrees.')
        else:
            units = units[:3]
        tempX = self._component[0]
        tempY = self._component[1]
        r = sqrt(tempX ** 2 + tempX ** 2)
        # Vector points along the positive x-axis
        if tempX > 0 and tempY == 0:
            theta = 0
        # Vector is in the first quadrant
        elif tempX > 0 and tempY > 0:
            theta = atan(tempY / tempX)
        # Vector points along the positive y-axis
        elif tempX == 0 and tempY > 0: 
            theta = pi / 2
        # Vector is in the second quadrant
        elif tempX < 0 and tempY > 0:
            theta = atan(tempY / abs(tempX)) + (pi / 2)
        # Vector points along the negative x-axis
        elif tempX < 0 and tempY == 0:
            theta = pi
        # Vector is in the third quadrant
        elif tempX < 0 and tempY < 0:
            theta = atan(abs(tempY) / abs(tempX)) + pi
        # Vector points along the negative y-axis
        elif tempX == 0 and tempY < 0:
            theta = (3 * pi) / 2
        # Vector is in the fourth quadrant
        else:
            theta = atan(abs(tempY) / tempX) + ((3 * pi) / 2)
        if units == "deg":
            theta = theta * 180 / pi
        return [r, theta]
    
    @property            
    def x(self):
        return self._head[0]
    
    @property
    def y(self):
        return self._head[1]