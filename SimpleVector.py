# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 04:46:51 2019

@author: Chris Mitchell

SimpleVector is a generic vector class for mathematical usage. This vector is
defined to be useful in performing vector operations in vector calculus and
linear algebra. Other Python libraries such as NumPy have much more efficient
vector and matrix operations.

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
    
Vector operations of vectors with different tail coordinates will always
be calculated by shifting the second vector given to the origin first.

TO DO:
    
    . Modify doctest to be more comprehensive
    . Implement simple graphing


"""

from math import sqrt

class SimpleVector:
    """
    A class for a generic mathematical vector. This is an immutable object.
    
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
    norm : float, complex
        The Euclidean norm of the vector
    origin : list
        A list containing the origin
    tail : list
        A list containing the tail coordinates of the vector.
    zero : vector
        The zero vector

    Methods
    -------   
    dot : vector
        Returns the dot product of both vectors
    proj : vector
        Returns the vector projected onto the argument
    scale : int, float, complex
        Returns a vector in the direction of self scaled to the given
        magnitude.
    shift : list, optional
        Shift the tail of the vector to a new point. If no point is specified,
        the vector is shifted to the origin
    unit :
        Return the vector as a unit vector
        
    """
    
    def __init__(self, head, tail = []):
        """
        Initialize the vector object using a list. A tail can also be
        provided as a list. If specified, it must be the same dimension as
        the head. If not specified, the tail will be assumed to be
        at the origin.
        
        Parameters
        ----------
        head : list, vector
            This is either an ordered list of components or another vector
        tail : list, optional
            This is an ordered list of components of the vector tail
        
        Raises
        ------
        TypeError
            If an unexpected type is passed in as head or tail or
            if the list components are not all numbers
        Exception
            An exception for all other init errors
        """
        
        #If a vector is provided as an argument to the constructor,
        #copy the attributes or the existing vector and return.
        if isinstance(head, __class__):
            self._head = head._head.copy()
            self._tail = head._tail.copy()
            self._dim = head._dim
            self._dtype = head._dtype
            self._origin = head._origin.copy()
            self._component = head._component.copy()
            self._norm = head._norm
            return
        
        #Initialize _components and test whether the constructor is called
        #with a list of numeric values.
        try:
            self._head = list(head)
        except TypeError:
            raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
        except:
            raise Exception("Unknown error in class constructor.")

        #Check if components are numbers.
        self._checkListNumeric(self._head)
            
        #Initialize the tail if given. If the tail is all zeros, then
        #the list will remain empty.
        try:
            self._tail = list(tail)
        except TypeError:
            print("Expected list or similar castable object as tail. Got " + str(type(tail)) + ".")
        except:
            raise Exception("Unknown error in class constructor.")

        #If the tail is specified, check that the entries are numbers and
        #that it is of the same dimension as the vector itself.
        if self._tail != []:                
            self._checkListNumeric(self._tail)
            if len(self._tail) != len(self._head):
                raise Exception("The specified tail does not have the same dimension as the head.")
 
        #Set _dim to be the dimensions of the vector.
        self._dim = len(self._head)

        #Upcast the head and the tail if necessary and set _dtype.      
        complexNum = False
        floatNum = False

        for i in self._head:
            if type(i) == float: floatNum = True
            elif type(i) == complex: complexNum = True
                
        if complexNum:
            self._head = [complex(i) for i in self._head]
            self._tail = [complex(i) for i in self._tail]
            self._dtype = complex
        elif not complexNum and floatNum:
            self._head = [float(i) for i in self._head]
            self._tail = [float(i) for i in self._tail]
            self._dtype = float
        else:
            self._dtype = int
            
        #Set the origin
        self._origin = [0 for i in range(self._dim)]
        
        #Set the component form of the vector as head - tail
        self._component = self._componentForm()
        
        #Set the norm
        self._norm = self._euclideanNorm()
                
    def __repr__(self):
        """
        Vector output will be different from that of a list. First, angle
        brackets will be used instead of square brackets. If a tail is
        specified, then the coordinates of the head and tail will be printed 
        as tail->head.
        """
        
        if self._tail == []:
            return '\u27e8{}\u27e9'.format(', '.join(['{}' for _ in self._head])).format(*self._head)
        else:
            return '({})\u27f6({})'.format(', '.join(['{}' for i in self._tail]),', '.join(['{}' for i in self._head])).format(*self._tail, *self._head)

    def __str__(self):
        """
        Use __repr__.
        """
        return self.__repr__()
    
    #Other private methods:
    
    def __abs__(self):
        return self.norm
    
    def __add__(self, other):
        """
        Vector addition
        """
        self._checkCompatability(other)
        if self._tail == []:
            return self._construct([self._component[i] + other._component[i] for i in range(self._dim)])
        else:
            return self._construct([self._component[i] + other._component[i] + self._tail[i] for i in range(self._dim)], tail = self._tail)

    def __and__(self, other):
        return NotImplemented
    
    def __bool__(self):
        if self.norm != 0:
            return True
        else:
            return False
    
    def __complex__(self):
        self._dtype = complex
        if self._tail == []:
            return self._construct([complex(i) for i in self._head], tail = [])
        else:
            return self._construct([complex(i) for i in self._head], tail = [complex(i) for i in self._tail])
        
    def __divmod__(self, other):
        return NotImplemented
        
    def __eq__(self, other):
        """
        Vector equality
        """
        self._checkCompatability(other)
        equality = True
        for i in range(self._dim):
            if self._component[i] != other._component[i]:
                equality = False
        return equality

    def __float__(self):
        self._dtype = float
        if self._tail == []:
            return self._construct([float(i) for i in self._head], tail = [])
        else:
            return self._construct([float(i) for i in self._head], tail = [float(i) for i in self._tail])
    
    def __floordiv__(self, other):
        """
        Componentwise or scalar integer division.
        """
        if isinstance(other, __class__):
            self._checkCompatability(other)
            if self._tail == []:
                return self._construct([self._component[i] // other._component[i] for i in range(self._dim)])
            else:                
                return self._construct([(self._component[i] // other._component[i]) + self._tail[i] for i in range(self._dim)], tail = self._tail)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._head[i] // other for i in range(self._dim)], tail = self._tail)
        
    def __getitem__(self, index):
        """
        Return the proper head coordinate.
        """
        return self._head[index]
    
    def __ge__(self, other):
        self._checkCompatability(other)
        if self.norm >= other.norm:
            return True
        else:
            return False
    
    def __gt__(self, other):
        self._checkCompatability(other)
        if self.norm > other.norm:
            return True
        else:
            return False
        
    def __iadd__(self, other):
        return self.__add__(other)
    
    def __iand__(self, other):
        return NotImplemented
    
    def __ifloordiv__(self, other):
        return self.__floordiv__(other)
    
    def __ilshift__(self, other):
        return NotImplemented
    
    def __imatmul__(self, other):
        return self.__matmul__(other)
    
    def __imod__(self, other):
        return self.__mod__(other)
    
    def __imul__(self, other):
        return self.__mul__(other)
    
    def __int__(self):
        self._dtype = int
        if self._tail == []:
            return self._construct([int(i) for i in self._head], tail = [])
        else:
            return self._construct([int(i) for i in self._head], tail = [int(i) for i in self._tail])
    
    def __invert__(self):
        return self.__neg__()
    
    def __ior__(self, other):
        return NotImplemented
    
    def __ipow__(self, other):
        return self.__pow__(other)

    def __irshift__(self, other):
        return NotImplemented
    
    def __isub__(self, other):
        return self.__sub__(other)
    
    def __itruediv__(self, other):
        return self.__truediv__(other)
    
    def __ixor__(self, other):
        return NotImplemented
    
    def __le__(self, other):
        self._checkCompatability(other)
        if self.norm <= other.norm:
            return True
        else:
            return False
    
    def __len__(self):
        return self._dim
    
    def __lshift__(self, other):
        return NotImplemented
    
    def __lt__(self, other):
        self._checkCompatability(other)
        if self.norm < other.norm:
            return True
        else:
            return False
    
    def __matmul__(self, other):
        """
        Return the dot product.
        """
        self.dot(other)
        
    def __mod__(self, other):
        """
        Componentwise or scalar modulus.
        """
        if isinstance(other, __class__):
            self._checkCompatability(other)
            if self._tail == []:
                return self._construct([self._component[i] % other._component[i] for i in range(self._dim)])
            else:                
                return self._construct([(self._component[i] % other._component[i]) + self._tail[i] for i in range(self._dim)], tail = self._tail)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._head[i] % other for i in range(self._dim)], tail = self._tail)
        
    def __mul__(self, other):
        """
        Componentwise or scalar multiplication.
        """
        if isinstance(other, __class__):
            self._checkCompatability(other)
            if self._tail == []:
                return self._construct([self._component[i] * other._component[i] for i in range(self._dim)])
            else:                
                return self._construct([(self._component[i] * other._component[i]) + self._tail[i] for i in range(self._dim)], tail = self._tail)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._head[i] * other for i in range(self._dim)], tail = self._tail)
        
    def __ne__(self, other):
        """
        Vector equality
        """
        self._checkCompatability(other)
        inequality = True
        for i in range(self._dim):
            if self._component[i] == other._component[i]:
                inequality = False
        return inequality
        
    def __neg__(self):
        return self._construct([self._head[i] * -1 for i in range(self._dim)], tail = self._tail)
    
    def __or__(self, other):
        return NotImplemented

    def __pos__(self):
        """
        Do nothing but return a new vector.
        """
        return self._construct(self._head, tail = self._tail)
    
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
                return self._construct(self._head, tail = self._tail)
            else:
                return self._construct([dotProductPower * self._head[i] for i in range(self._dim)], tail = self._tail)
        
    def __radd__(self, other):
        """
        Will never be called.
        """
        pass
    
    def __rand__(self, other):
        return NotImplemented
    
    def __rdivmod__(self, other):
        return NotImplemented

    def __rfloordiv__(self, other):
        """
        Scalar // Vector is not a defined operation on vectors.
        """
        return NotImplemented
    
    def __rlshift__(self, other):
        return NotImplemented
    
    def __rmatmul__(self, other):
        """
        Will never be called.
        """
        pass
    
    def __rmod__(self, other):
        """
        Scalar % Vector is not a defined operation on vectors.
        """
        return NotImplemented

    def __rmul__(self, other):
        """
        Scalar multiplication with scalar first.
        """
        return self.__mul__(other)
    
    def __ror__(self, other):
        return NotImplemented
    
    def __rpow__(self, other):
        """
        Scalar ** Vector is not a defined operation on vectors.
        """
        return NotImplemented
    
    def __rrshift__(self, other):
        return NotImplemented
    
    def __rshift__(self, other):
        return NotImplemented
    
    def __rsub__(self, other):
        """
        Will never be called.
        """
        pass
    
    def __rtruediv__(self, other):
        """
        Scalar / Vector is not a defined operation on vectors.
        """
        return NotImplemented
    
    def __rxor__(self, other):
        return NotImplemented
                 
    def __sub__(self, other):
        """
        Componentwise subtraction.
        """
        self._checkCompatability(other)
        if self._tail == []:
            return self._construct([self._component[i] - other._component[i] for i in range(self._dim)])
        else:
            return self._construct([self._component[i] - other._component[i] + self._tail[i] for i in range(self._dim)], tail = self._tail)
    
    def __truediv__(self, other):
        """
        Componentwise or scalar division.
        """
        if isinstance(other, __class__):
            self._checkCompatability(other)
            if self._tail == []:
                return self._construct([self._component[i] / other._component[i] for i in range(self._dim)])
            else:                
                return self._construct([(self._component[i] / other._component[i]) + self._tail[i] for i in range(self._dim)], tail = self._tail)
        else:
            self._checkComponentNumeric(other)
            return self._construct([self._head[i] / other for i in range(self._dim)], tail = self._tail)

    def __xor__(self, other):
        return NotImplemented

    @property
    def component(self):
        return self._componentForm()

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
        return self._head

    @property
    def inverse(self):
        """
        Return additive inverse as a vector.
        """
        return self._construct(-self, tail = self._tail)
    
    @property
    def norm(self):
        """
        Return the Euclidean norm of the vector.
        """
        return self._norm
    
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
        return self._tail
    
    @property
    def zero(self):
        """
        Return the zero vector.
        """
        return self._construct([0 for i in range(self._dim)])
    
    @classmethod
    def _construct(cls, head, tail = []):
        """
        A special class method which makes certain that child classes of
        SimpleVector are returned instances of the child class.
        """
        return cls(head, tail)

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
        
    def _checkCompatability(self, other):
        """
        A type check to make sure that operations between vectors are
        specified using the vector class and that they share both dimension.
        """
        if not isinstance(other, __class__):
            raise TypeError("Both arguments must be of the vector class.")
        if self._dim != other._dim:
            raise Exception("Vectors are of unequal dimension.")
            
    def _componentForm(self):
        """
        Return the component form of the vector.
        """
        if self._tail == []:
            return self._head.copy()
        else:
            return [self._head[i] - self._tail[i] for i in range(self._dim)]
        
    def _euclideanNorm(self):
        """
        Compute the Euclidean norm of a vector.
        
        Parameters
        ----------
        None
        
        Returns
        -------
        int, float, or complex
            The norm of the vector
        
        """
        euclideanNorm = 0
        for i in range(self._dim):
            euclideanNorm += (self._component[i]) ** 2
        return sqrt(euclideanNorm)
    
    def dot(self, other):
        """
        Compute the dot product of two vectors.
        
        Parameters
        ----------
        other : vector
            A vector-type class.
            
        Returns
        -------
        int, float, complex
            The calculated dot product will be of type _dtype
            
        """
        self._checkCompatability(other)
        dotProduct = 0
        for i in range(self._dim):
            dotProduct += self._component[i] * other._component[i]
        return dotProduct
    
    def proj(self, other):
        """
        Return the projection of self onto other:
                        a . b 
           a.proj(b) =  ----- * b
                        b . b
                        
        Parameters
        ----------
        other : vector
            A vector-type class
            
        Returns
        -------
        vector
            The projection of self onto other
            
        """
        self._checkCompatability(other)
        scalar = self.dot(other) / other.norm
        return self._construct(scalar * other, tail = self.tail)
    
    def scale(self, magnitude):
        """
        Return a vector in the direction of self scaled to a given magnitude.
        
        Parameters
        ----------
        magnitude : int, float, complex
        
        Returns
        -------
        vector
            The same vector scaled.
            
        """
        unit = self.unit()
        return magnitude * unit
    
    def shift(self, newTail = []):
        """
        Shift the vector to a new point. The new tail must be specified
        as a list with the same dimension as the Vector. If the tail is
        not specified, the vector tail is shifted to [0, 0, ...].
        
        Parameters
        ----------
        newTail : list, optional
            The new coordinates to which to shift the tail of the vector
            
        Returns
        -------
        vector
            A vector-type class
            
        """
        if newTail == [] and self._tail == []:
            return self._construct(self)
        elif newTail == [] and self._tail != []:
            return self._construct([self._component[i] for i in range(self._dim)], tail = [])
        else:
            if len(newTail) != self._dim:
                raise Exception("Shift is not the same dimension as Vector.")
            else:
                return self._construct([self._component[i] + newTail[i] for i in range(self._dim)], tail = newTail)
    
    def unit(self):
        """
        Return the vector as a unit vector:
                        v            
            a.unit() = ---
                       |v|
                       
        Parameters
        ----------
        None
        
        Returns
        -------
        vector
            A vector-class type
            
        """
        if self._tail == []:
            return self._construct([self._component[i] / self.norm for i in range(self._dim)])
        else:
            return self._construct([(self._component[i] / self.norm) + self._tail[i] for i in range(self._dim)], tail = self._tail)
    
 