# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:51 2019

@author: Chris Mitchell

A vector class for mathematical usage. This vector is defined to be useful
in seeing the operations of vector calculus and linear algebra. Other Python
libraries have much more efficient vector and matrix operations.
"""

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
                print("Expected list or similar castable object as vector. Got " + type(head) + ".")
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
                print("Expected list or similar castable object as origin. Got " + type(origin) + ".")
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
            return str(self._coordinates)
        else:
            return str(self._origin) + " -> " + str(self._coordinates)

    def __str__(self):
        return self.__repr__()
    
    def __add__(self, other):
        self._checkTypeCompatability(other)
        if self._origin == []:
            return Vector([self._coordinates[i] + other._coordinates[i] for i in range(self._dim)])
        else:
            return Vector([self._coordinates[i] + other._coordinates[i] for i in range(self._dim)], origin = self._origin)
        
    def __sub__(self, other):
        self._checkTypeCompatability(other)
        if self._origin == []:
            return Vector([self._coordinates[i] - other._coordinates[i] for i in range(self._dim)])
        else:
            return Vector([self._coordinates[i] - other._coordinates[i] for i in range(self._dim)], origin = self._origin)

    def __mul__(self, other):
        raise Exception("Multiplication with vectors is ambiguous. Please use either the dot() or cross() methods.")
        
    def _undef(self):
        raise Exception("This operation is undefined on vectors.")

    def _checkTypeCompatability(self, other):
        if type(other) != Vector:
            raise TypeError("Second argument is not of the Vector class.")
        if len(self._coordinates) != len(other._coordinates):
            raise Exception("Vectors are of unequal dimension.")
        if self._origin != other._origin:
            raise Exception("Specified origins do not match.")
        
    def add(self, other):
        return self.__add__(other)
    
    def sub(self, other):
        return self.__sub__(other)
    
                
            
