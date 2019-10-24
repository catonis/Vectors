# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:51 2019

@author: Chris Mitchell

A vector class for mathematical usage. This vector is defined to be useful
in seeing the operations of vector calculus and linear algebra. Other Python
libraries have much more efficient vector and matrix operations.
"""

from math import sqrt

class Vector:
    
    def __init__(self, head, axis = 0, origin = []):
        """Initialize the vector object using a list. An axis is provided
           to delineate whether this is a row or column vector. The default
           is a row vector."""
        
        #Initialize _coordinates and test whether the constructor is called
        #with a list of numeric values.
        if type(head) == list:
            self._coordinates = head
        else:
            try:
                self._coordinates = list(head)
            except TypeError:
                raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
            except:
                raise Exception("Unknown error in class constructor.")
        
        #Check if entries are numbers.

        for i in self._coordinates:
            if not bool(0 == i * 0):
                raise Exception("Vector list elements must be numbers.")
            
        #Initialize axis with either 0 or 1.
        if type(axis) == int and (axis == 0 or axis == 1):
            self._axis = axis
        elif type(axis) == str:
            if axis == "row": self._axis = 0
            elif axis == "column": self._axis = 1
            else: raise Exception('Expected axis to be 0, 1, "row," or "column".')
        
        
        #Initialize the origin if given. If the origin is all zeros, then
        #the list will remain empty.
        if type(origin) == list:
            self._origin = origin
        else:
            try:
                self._origin = list(origin)
            except TypeError:
                print("Expected list or similar castable object as origin. Got " + str(type(origin)) + ".")
            except:
                raise Exception("Unknown error in class constructor.")

        if self._origin != []:                
            for i in self._origin:
                if not bool(0 == i * 0):
                    raise Exception("Origin list elements must be numbers.")
            if len(self._origin) != len(self._coordinates):
                raise Exception("The specified origin is not the same length as the vector.")
 
        #Upcast the vector and the origin if necessary and set _dtype.      
        complexNum = False
        floatNum = False

        for i in self._coordinates:
            if type(i) == float: floatNum = True
            elif type(i) == complex: complexNum = True
                
        if complexNum:
            self._coordinates = [complex(i) for i in self._coordinates]
            self._origin = [complex(i) for i in self._origin]
            self._dtype = complex
        elif not complexNum and floatNum:
            self._coordinates = [float(i) for i in self._coordinates]
            self._origin = [float(i) for i in self._origin]
            self._dtype = float
        else:
            self._dtype = int
            
        #Set _dim to be the dimensions of the vector.
        self._dim = len(self._coordinates)

        #Initialization and type check complete.
    
    def __repr__(self):
        if self._origin == []:
            return '\u27e8' + str(self._coordinates)[1:-1] + '\u27e9'
        else:
            return '\u27e8' + str(self._origin)[1:-1] + '\u27e9 \u27f6 \u27e8' + str(self._coordinates)[1:-1] + '\u27e9'

    def __str__(self):
        return self.__repr__()
    
    def __add__(self, other):
        self._checkTypeCompatability(other)
        return Vector([self._coordinates[i] + other._coordinates[i] for i in range(self._dim)], origin = self._origin, axis = self._axis)
        
    def __sub__(self, other):
        self._checkTypeCompatability(other)
        return Vector([self._coordinates[i] - other._coordinates[i] for i in range(self._dim)], origin = self._origin, axis = self._axis)

    def __mul__(self, other):
        if bool(0 == other * 0):
            return Vector([self._coordinates[i] * other for i in range(self._dim)], origin = self._origin, axis = self._axis)
        else:
            raise Exception("Multiplication of vectors with non-scalars is ambiguous. Please use either the dot() or cross() methods.")
            
    def __div__(self, other):
        self._undef()
             
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def _undef(self):
        raise Exception("This operation is undefined on vectors.")

    def _checkTypeCompatability(self, other):
        if type(other) != Vector:
            raise TypeError("Both arguments must be of the Vector class.")
        if len(self._coordinates) != len(other._coordinates):
            raise Exception("Vectors are of unequal dimension.")
        if self._origin != other._origin:
            raise Exception("Specified origins must match.")
                    
    def add(self, other):
        return self.__add__(other)
    
    def sub(self, other):
        return self.__sub__(other)
    
    def smul(self, other):
        """Scalar multiplication."""
        return self.__mul__(other)
    
    def shift(self, newOrigin = []):
        """Shift the vector to a new origin. The new origin must be specified
           as a list with the same dimension as the Vector. If the origin is
           not specified, the origin is moved to [0, 0, ...]."""
        if newOrigin == [] and self._origin == []:
            return self
        elif newOrigin == [] and self._origin != []:
            return Vector([self._coordinates[i] - self._origin[i] for i in range(self._dim)], origin = [], axis = self._axis)
        else:
            if len(newOrigin) != self._dim:
                raise Exception("Shift is not the same dimension as Vector.")
            return Vector([self._coordinates[i] + newOrigin[i] for i in range(self._dim)], origin = newOrigin, axis = self._axis)

    def norm(self):
        euclideanNorm = 0.0
        if self._origin == []:
            tempOrigin = [0 for i in range(self._dim)]
        else:
            tempOrigin = self._origin
        for i in range(self._dim):
            euclideanNorm += (self._coordinates[i] - tempOrigin[i]) ** 2
        return sqrt(euclideanNorm)
    
    def dot(self, other):
        self._checkTypeCompatability(other)
        dotProduct = 0.0
        for i in range(self._dim):
            dotProduct += self._coordinates[i] * other._coordinates[i]
        return dotProduct

            
        
        
            
            
            
        
        
    
                
            