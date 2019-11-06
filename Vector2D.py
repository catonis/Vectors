# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 04:03:09 2019

@author: Chris Mitchell

Vector2D is a two-dimensional cartesian vector based on the generic class
SimpleVector. Its implementation restricts usage to two-dimensions and adds
methods to work with such vectors.

TO DO
    . Add docstrings for class and methods
    . Broaden doctest for all functions
    
"""

from math import sqrt, acos, atan, pi
from SimpleVector import SimpleVector

class Vector2D(SimpleVector):
    """
    A class for a two-dimensional vector.
    
    ...
    
    Attributes
    ----------
    component : list
        The component form of the vector, i.e.:
            <head[0] - tail[0], head[1] - tail[1], ...>
        If the vector has no specified tail, a copy of the list of
        coordinates is returned.
    dim, dimension : int
        The length or number of components of the vector
    dtype : type object
        The numeric type of the components (int, float, or complex)
    head : list
        A list containing the head coordinates of the vector
    inverse : vector
        The additive inverse of the vector
    origin : list
        A list containing the origin
    tail : list
        A list containing the tail coordinates of the vector.
    x : int, float, or complex
        The x-coordinate of the vector head
    y : int, float, or complex
        The y-coordinate of the vector head
    zero : vector
        The zero vector

    Methods
    -------   
    angle : vector; units, optional
        Returns the angle between two vectors in radians or degrees
    cosine : vector
        Returns the cosine of the angle between the two vectors
    dot : vector
        Returns the dot product of both vectors
    norm :
        Returns the Euclidean norm or length of the vector
    proj : vector
        Returns the vector projected onto the argument
    shift : list, optional
        Shift the tail of the vector to a new point. If no point is specified,
        the vector is shifted to the origin
    toPolar : units, optional
        Returns the polar coordinates of the vector head as a list [r, theta]
    unit :
        Return the vector as a unit vector
        
    """

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
        
    @property            
    def x(self):
        return self._head[0]
    
    @property
    def y(self):
        return self._head[1]

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
        """
        Returns the angle between self and other.
        
        Parameters
        ----------
        other : vector
            The vector for which the angle is defined
        units : {'rad', 'radians', 'deg', 'degrees'}
            Specify whether to return the angle in radians or degrees
            (defaults to radians)
            
        Returns
        -------
        float
            The angle between self and other in radians or degrees
            
        """
        
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
            return '\u27e8{0}, {1}\u27e9 = {2}\u27e8{3[0]}, {3[1]}\u27e9'.format(symbolX, symbolY, symbolT, self._head)
        else:
            return '\u27e8{0}, {1}\u27e9 = ({2[0]}, {2[1]}) + {3}\u27e8{4[0]}, {4[1]}\u27e9'.format(symbolX, symbolY, self._tail, symbolT, self._head)
        
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
    
    def cosine(self, other):
        """
        Returns the cosine of the angle between two vectors:
                         x . y
            cosTheta = ---------
                       |x| * |y|
                       
        Parameters
        ----------
        other : vector
            The vector for which we need the cosine of the angle.
            
        Returns
        -------
        float
            The cosine of the angle between the two vectors.
        
        """
        
        self._checkTypeCompatability(other)
        return self.dot(other) / (self.norm() * other.norm())   

    def toPolar(self, units = "rad"):
        """
        toPolar will return will return the vector in [r, theta] form,
        r being the length of the vector and theta being its angle from
        the positive x-axis. Both r and theta will always be positive and
        theta will be 0 <= theta < 2 * pi or 0 <= theta < 360 depending on
        selected units. If the tail is anywhere but the origin, the origin
        will be reset to (0, 0). If the vector is the zero vector, (0, 0)
        will be returned.

        
        Parameters
        ----------
        units : {'rad', 'radians', 'deg', 'degrees'}
            Specify whether to return the angle in radians or degrees
            
        Returns
        -------
        list
            [r, theta]
            
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
    
