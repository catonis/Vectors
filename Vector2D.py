# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 04:03:09 2019

@author: Chris Mitchell
"""

from SimpleVector import SimpleVector
from math import acos, asin, pi

class Vector2D(SimpleVector):

    def __init__(self, head, origin = []):
        
        if type(head) == Vector2D or type(head) == SimpleVector:
            if head._dim != 2:
                raise Exception("Vector2D can only be initialized with a two-dimensional vector.")
            else:
                self._components = head._components.copy()
                self._origin = head._origin.copy()
                self._dim = head._dim
                self._dtype = head._dtype
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
        super().__init__(head, origin)

    def _checkTypeCompatability(self, other):
        """
        A type check to make sure that operations between vectors are specified
        using the SimpleVector class or Vector2D clas and that they share both
        dimension and origin.
        """
        if type(other) != SimpleVector and type(other) != Vector2D:
            raise TypeError("Both arguments must be of the Vector2D class.")
        if other.dim != 2:
            raise Exception("Vectors are of unequal dimension.")
        if self._origin != other._origin:
            raise Exception("Specified origins must match.")

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
