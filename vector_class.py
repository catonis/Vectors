# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:51 2019

@author: Chris Mitchell

A vector class for mathematical usage. This vector is defined to be useful
in seeing the operations of vector calculus and linear algebra. Other Python
libraries have much more efficient vector and matrix operations.

TO DO:
    . Add verbosity for operations
    . Add functionality for a vector with complex components
    . Add cross product for 7-dim vectors
    . Add slicing
    
"""

from math import sqrt

class Vector:
    
    def __init__(self, head, axis = 0, origin = []):
        """Initialize the vector object using a list. An axis is provided
           to delineate whether this is a row or column vector. Currently,
           the axis is just a placeholder for the potential need. The default
           is a row vector. An origin can also be provided as a list. If
           specified, it must be the same dimension as the vector. If not
           specified, the origin will be assumed to be [0, 0, ...].
           
           The init method will also initialize to other variables:
           _dtype and _dim. The type of value specified in the head list
           will be stored in _dtype. The dimension of the head list will
           be stored in _dim."""
        
        #If a Vector is provided as an argument to the constructor,
        #copy the attributes or the existing vector and return.
        if type(head) == Vector:
            self._coordinates = head._coordinates.copy()
            self._origin = head._origin.copy()
            self._dim = head._dim
            self._dtype = head._dtype
            self._axis = head._axis
            return
        
        #Initialize _coordinates and test whether the constructor is called
        #with a list of numeric values.
        try:
            self._coordinates = list(head)
        except TypeError:
            raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
        except:
            raise Exception("Unknown error in class constructor.")


        #Check if coordinate entries are numbers.
        for i in self._coordinates:
            if not bool(0 == i * 0):
                raise Exception("Vector list elements must be numbers.")
            
        #Initialize axis with either 0 or 1. 
        if type(axis) == int and (axis == 0 or axis == 1):
            self._axis = axis
        elif type(axis) == str:
            if axis == "row": self._axis = 0
            elif axis == "column" or axis == "col": self._axis = 1
            else: raise Exception('Expected axis to be 0, 1, "row," or "column".')
        else:
            raise Exception('Expected axis to be 0, 1, "row," or "column".')
        
        #Initialize the origin if given. If the origin is all zeros, then
        #the list will remain empty.
        try:
            self._origin = list(origin)
        except TypeError:
            print("Expected list or similar castable object as origin. Got " + str(type(origin)) + ".")
        except:
            raise Exception("Unknown error in class constructor.")

        #If the origin is specified, check that the entries are numbers and
        #that it is of the same dimension as the vector itself.
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
        """Vector output will be different from that of a list. First, angle brackets
           will be used instead of square brackets. If an origin is specified, then
           the origin will be printed as well in the form of origin->vector."""
        if self._origin == []:
            return '\u27e8' + str(self._coordinates)[1:-1] + '\u27e9'
        else:
            return str(self._origin) + ' \u27f6 \u27e8' + str(self._coordinates)[1:-1] + '\u27e9'

    def __str__(self):
        """Use __repr__."""
        return self.__repr__()
    
    #Other private methods:
    
    def __add__(self, other):
        """Vector addition."""
        self._checkTypeCompatability(other)
        return Vector([self._coordinates[i] + other._coordinates[i] for i in range(self._dim)], origin = self._origin, axis = self._axis)
        
    def __div__(self, other):
        """Undefined. If division by a scalar is required, simply perform scalar
           multiplication using the reciprocal of the scalar."""
        self._undef()
        
    def __getitem__(self, index):
        return self._coordinates[index]

    def __mul__(self, other):
        """Scalar multiplication."""
        
        #Ensure we are given a scalar and nothing else.
        if bool(0 == other * 0):
            return Vector([self._coordinates[i] * other for i in range(self._dim)], origin = self._origin, axis = self._axis)
        else:
            raise Exception("Multiplication of vectors with non-scalars is ambiguous. Please use either the dot() or cross() methods.")           

    def __rmul__(self, other):
        """Scalar multiplication with operands in a different order."""
        return self.__mul__(other)
                 
    def __sub__(self, other):
        """Vector subtraction."""
        self._checkTypeCompatability(other)
        return Vector([self._coordinates[i] - other._coordinates[i] for i in range(self._dim)], origin = self._origin, axis = self._axis)

    @property            
    def dim(self):
        return self._dim
    
    @property
    def dimension(self):
        return self._dim
    
    @property
    def dtype(self):
        return self._dtype
    
    @property
    def axis(self):
        return self._axis
    
    @property
    def origin(self):
        """Return as a list."""
        return self._origin
    
    @property
    def tail(self):
        """Return as a list."""
        return self._origin
    
    @property
    def head(self):
        """Return as a list."""
        return self._coordinates
        
    def _undef(self):
        """A catch-all method to be called if a mathematical operation is undefined."""
        raise Exception("This operation is undefined on vectors.")

    def _checkTypeCompatability(self, other):
        """A type check to make sure that operations between vectors are specified
           using the Vector class."""
        if type(other) != Vector:
            raise TypeError("Both arguments must be of the Vector class.")
        if len(self._coordinates) != len(other._coordinates):
            raise Exception("Vectors are of unequal dimension.")
        if self._origin != other._origin:
            raise Exception("Specified origins must match.")
                    
    def add(self, other):
        """A direct method for the addition of two vectors."""
        return self.__add__(other)
    
    def sub(self, other):
        """A direct method for the subtraction of two vectors."""
        return self.__sub__(other)
    
    def smul(self, other):
        """A direct method for scalar multiplication."""
        return self.__mul__(other)
    
    def shift(self, newOrigin = []):
        """Shift the vector to a new origin. The new origin must be specified
           as a list with the same dimension as the Vector. If the origin is
           not specified, the origin is moved to [0, 0, ...]."""
        if newOrigin == [] and self._origin == []:
            return Vector(self)
        elif newOrigin == [] and self._origin != []:
            return Vector([self._coordinates[i] - self._origin[i] for i in range(self._dim)], origin = [], axis = self._axis)
        else:
            if len(newOrigin) != self._dim:
                raise Exception("Shift is not the same dimension as Vector.")
            return Vector([self._coordinates[i] + newOrigin[i] for i in range(self._dim)], origin = newOrigin, axis = self._axis)

    def norm(self):
        """Compute the Euclidean norm of a vector. This is the same as length
           in a Euclidean space. The norm is returned as a float."""
        euclideanNorm = 0.0
        if self._origin == []:
            tempOrigin = [0 for i in range(self._dim)]
        else:
            tempOrigin = self._origin
        for i in range(self._dim):
            euclideanNorm += (self._coordinates[i] - tempOrigin[i]) ** 2
        return sqrt(euclideanNorm)
    
    def dot(self, other):
        """Compute the dot product of two vectors. The dot product is returned as
           a float."""
        self._checkTypeCompatability(other)
        dotProduct = 0
        for i in range(self._dim):
            dotProduct += self._coordinates[i] * other._coordinates[i]
        return dotProduct
    
    def cross(self, other):
        """Compute the cross product of two, three-dimensional vectors."""
        if self._dim != 3 or other._dim != 3:
            raise Exception("The cross product is only defined for 3-dimensional vectors.")
        self._checkTypeCompatability(other)
        newVec = []
        newVec.append(self[1] * other[2] - self[2] * other[1])
        newVec.append(self[0] * other[2] - self[2] * other[0])
        newVec.append(self[0] * other[1] - self[1] * other[0])
        return Vector(newVec, origin=self.origin)
    
    def proj(self, other):
        self._checkTypeCompatability(other)
        scalar = self.dot(other) / other.norm()
        return Vector(scalar * other, origin = self.origin, axis = self.axis)
