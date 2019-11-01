# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:51 2019

@author: Chris Mitchell

A vector class for mathematical usage. This vector is defined to be useful
in seeing the operations of vector calculus and linear algebra. Other Python
libraries such as NumPy have much more efficient vector and matrix operations.

As a SimpleVector, the class will implement vector attributes and methods
which satisfy the axioms of a vector space. This includes:
    
    . Componentwise and Scalar Vector Addition (and Subtraction)
    . Componentwise and Scalar Vector Multiplication (and Division)
    . Dot or Inner Product
    . Euclidean Norm
    . Additive Identity
    . Additive Inverse
    . Negative Vector
    . Scalar Multiplication
    . Zero Vector

TO DO:


"""

from math import sqrt

class SimpleVector:
    """
    A class for a simple mathematical vector. This is an immutable object.
    
    ...
    
    Attributes
    ----------
    dim, dimension : int
        The length or number of components of the vector
    dtype : type object
        The numeric type of the components (int, float, or complex)
    head : list
        A list containing the vector components
    inverse : vector
        The additive inverse of the vector
    origin, tail : list
        A list containing the origin
    tail : list
        The tail or origin of the vector
    zero : vector
        The zero vector or multiplicative inverse of the vector

    Methods
    -------
    __add__ : vector
        Add two vectors
    __getitem__ :
        Allows for compoonent indexing
    __iter__ :
        Iterate over the vector components
    __len__ :
        Return the dimension of a vector
    __mul__ : scalar, vector
        Performs componentwise multiplication between two vectors or a
        vector and a scalar
    __neg__ :
        Provide a vector of the same length in the opposite direction
    __pos__ :
        Returns the vector
    __pow__ : int
        Raise vector to a given power. If the power is odd, the result is
        a vector. If even, the result is a scalar
    __rmul__ : scalar
        Returns the same value as __mul__ but provides a definition if
        the scalar is given after the vector.        
    __sub__ : vector
        Subtract two vectors
    __truediv__ : scalar, vector
        Performs componentwise division between two vectors or a vector
        and a scalar
    dot : vector
        Returns the dot product of both vectors
    norm :
        Returns the Euclidean norm or length of the vector
    proj : vector
        Returns the vector projected onto the argument
    shift : list, optional
        Shift the tail of the vector to a new point. If no point is specified,
        the vector is shifted to the origin
    unit :
        Return the vector as a unit vector
        
    """
    
    def __init__(self, head, origin = []):
        """
        Initialize the vector object using a list. An origin can also be
        provided as a list. If specified, it must be the same dimension as
        the vector. If not specified, the origin will be assumed to be
        [0, 0, ...].
        
        Parameters
        ----------
        head : list, vector
            This is either an ordered list of components or another vector
        origin : list, optional
            This is an ordered list of components of the vector tail
        
        Raises
        ------
        TypeError
            If an unexpected type is passed in as head or origin or
            if the list components are not all numbers
        Exception
            An exception for all other init errors
        """
        
        #If a vector is provided as an argument to the constructor,
        #copy the attributes or the existing vector and return.
        if isinstance(head, __class__):
            self._components = head._components.copy()
            self._origin = head._origin.copy()
            self._dim = head._dim
            self._dtype = head._dtype
            return
        
        #Initialize _components and test whether the constructor is called
        #with a list of numeric values.
        try:
            self._components = list(head)
        except TypeError:
            raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
        except:
            raise Exception("Unknown error in class constructor.")

        #Check if components are numbers.
        self._checkListNumeric(self._components)
            
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
            self._checkListNumeric(self._origin)
            if len(self._origin) != len(self._components):
                raise Exception("The specified origin does not have the same dimension as the vector.")
 
        #Upcast the vector and the origin if necessary and set _dtype.      
        complexNum = False
        floatNum = False

        for i in self._components:
            if type(i) == float: floatNum = True
            elif type(i) == complex: complexNum = True
                
        if complexNum:
            self._components = [complex(i) for i in self._components]
            self._origin = [complex(i) for i in self._origin]
            self._dtype = complex
        elif not complexNum and floatNum:
            self._components = [float(i) for i in self._components]
            self._origin = [float(i) for i in self._origin]
            self._dtype = float
        else:
            self._dtype = int
            
        #Set _dim to be the dimensions of the vector.
        self._dim = len(self._components)
    
    def __repr__(self):
        """
        Vector output will be different from that of a list. First, angle
        brackets will be used instead of square brackets. If an origin is
        specified, then the origin will be printed as well in the form of
        origin->vector.
        """
        
        if self._origin == []:
            return '\u27e8' + str(self._components)[1:-1] + '\u27e9'
        else:
            return '(' + str(self._origin)[1:-1] + ') \u27f6 \u27e8' + str(self._components)[1:-1] + '\u27e9'

    def __str__(self):
        """
        Use __repr__.
        """
        return self.__repr__()
    
    #Other private methods:
    
    def __add__(self, other):
        """
        Componentwise addition.
        """
        self._checkTypeCompatability(other)
        return self._construct([self._components[i] + other._components[i] for i in range(self._dim)], origin = self._origin)
        
    def __getitem__(self, index):
        return self._components[index]
    
    def __iter__(self):
        return iter(self._components)
    
    def __len__(self):
        return self._dim
        
    def __mul__(self, other):
        """
        Componentwise or scalar multiplication.
        """
        if isinstance(other, __class__):
            self._checkTypeCompatability(other)
            return self._construct([self._components[i] * other._components[i] for i in range(self._dim)], origin = self._origin)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._components[i] * other for i in range(self._dim)], origin = self._origin)
        
    def __neg__(self):
        return self._construct([self._components[i] * -1 for i in range(self._dim)], origin = self._origin)

    def __pos__(self):
        """
        Do nothing.
        """
        return self._construct(self._components, origin = self._origin)
    
    def __pow__(self, other):
        """
        Scalar powers of a given vector using the dot product:
            v ** 2 = v . v       : scalar
            v ** 3 = (v . v) * v : vector
        """
        if type(other) != int:
            raise Exception("Fractional powers or other objects are not defined for vector exponentiation.")
        dotProductPower = self.dot(self) ** (other // 2)
        if other % 2 == 0:
            return dotProductPower
        else:
            if other == 1:
                return self._construct(self._components, origin = self._origin)
            else:
                return self._construct([dotProductPower * self._components[i] for i in range(self._dim)], origin = self._origin)

    def __rmul__(self, other):
        """
        Scalar multiplication with scalar first.
        """
        return self.__mul__(other)
                 
    def __sub__(self, other):
        """
        Componentwise subtraction.
        """
        self._checkTypeCompatability(other)
        return self._construct([self._components[i] - other._components[i] for i in range(self._dim)], origin = self._origin)
    
    def __truediv__(self, other):
        """
        Componentwise or scalar division.
        """
        if isinstance(other, __class__):
            self._checkTypeCompatability(other)
            return self._construct([self._components[i] / other._components[i] for i in range(self._dim)], origin = self._origin)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._components[i] / other for i in range(self._dim)], origin = self._origin)

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
    def head(self):
        """
        Return as a list.
        """
        return self._components

    @property
    def inverse(self):
        """
        Return additive inverse as a vector.
        """
        return self._construct(-self, origin = self._origin)
    
    @property
    def origin(self):
        """
        Return as a list.
        """
        return self._origin
    
    @property
    def tail(self):
        """
        Return as a list.
        """
        return self._origin
    
    @property
    def zero(self):
        """
        Return the zero vector.
        """
        return self._construct([0 for i in range(self._dim)])
    
    @classmethod
    def _construct(cls, head, origin = []):
        return cls(head, origin)

    def _checkComponentNumeric(self, testVal):
        """
        Check if a given value is numeric.
        """
        if not bool(0 == testVal * 0):
            raise Exception("Specified value is not a numeric type.")
    
    def _checkListNumeric(self, testList):
        """
        Check if a given list contains numeric values.
        """
        for i in testList:
            if not bool(0 == i * 0):
                raise Exception("List components are not all numeric types.")
        
    def _checkTypeCompatability(self, other):
        """
        A type check to make sure that operations between vectors are
        specified using the vector class and that they share both dimension
        and origin.
        """
        if not isinstance(other, __class__):
            raise TypeError("Both arguments must be of the vector class.")
        if len(self._components) != len(other._components):
            raise Exception("Vectors are of unequal dimension.")
        if self._origin != other._origin:
            raise Exception("Specified origins must match.")
    
    def dot(self, other):
        """
        Compute the dot product of two vectors.
        """
        self._checkTypeCompatability(other)
        dotProduct = 0
        for i in range(self._dim):
            dotProduct += self._components[i] * other._components[i]
        return dotProduct

    def norm(self):
        """
        Compute the Euclidean norm of a vector.
        """
        euclideanNorm = 0
        if self._origin == []:
            tempOrigin = [0 for i in range(self._dim)]
        else:
            tempOrigin = self._origin
        for i in range(self._dim):
            euclideanNorm += (self._components[i] - tempOrigin[i]) ** 2
        return sqrt(euclideanNorm)
    
    def proj(self, other):
        """
        Return the projection of self onto other:
                        a . b 
           a.proj(b) =  ----- * b
                        b . b
        """
        self._checkTypeCompatability(other)
        scalar = self.dot(other) / other.norm()
        return self._construct(scalar * other, origin = self.origin)
    
    def shift(self, newOrigin = []):
        """
        Shift the vector to a new origin. The new origin must be specified
        as a list with the same dimension as the Vector. If the origin is
        not specified, the vector tail is shifted to [0, 0, ...].
        """
        if newOrigin == [] and self._origin == []:
            return self._construct(self)
        elif newOrigin == [] and self._origin != []:
            return self._construct([self._components[i] - self._origin[i] for i in range(self._dim)], origin = [])
        else:
            if len(newOrigin) != self._dim:
                raise Exception("Shift is not the same dimension as Vector.")
            return self._construct([self._components[i] + newOrigin[i] for i in range(self._dim)], origin = newOrigin)
    
    def unit(self):
        """
        Return the vector as a unit vector.
        """
        return self._construct([self._components[i] / self.norm() for i in range(self._dim)], origin = [])
    
 