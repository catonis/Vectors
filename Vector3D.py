# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 04:59:33 2019

@author: Chris Mitchell

Vector3D is a three-dimensional cartesian vector based on the generic class
SimpleVector. Its implementation restricts usage to three-dimensions and adds
methods to work with such vectors.

TO DO
    . Add docstrings for class and methods
    . Create doctest for all functions
    
"""

from math import sqrt, acos, asin, atan, pi
from SimpleVector import SimpleVector

class Vector3D(SimpleVector):
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
    norm : float, complex
        The Euclidean norm of the vector
    origin : list
        A list containing the origin
    tail : list
        A list containing the tail coordinates of the vector.
    x : int, float, or complex
        The x-coordinate of the vector head
    y : int, float, or complex
        The y-coordinate of the vector head
    z : int, float, or complex
        The z-coordinate of the vector head
    zero : vector
        The zero vector

    Methods
    -------   
    angle : vector; units, optional
        Returns the angle between two vectors in radians or degrees
    cross : vector
        Returns the cross product of both vectors as a Vector3D object
    proj : vector
        Returns the vector projected onto the argument
    scale : int, float, complex
        Returns a vector in the direction of self scaled to the given
        magnitude.
    shift : list, optional
        Shift the tail of the vector to a new point. If no point is specified,
        the vector is shifted to the origin
    sine : vector
        Returns the sine of the angle between the two vectors
    toCylindrical : units, optional
        Returns the cylindrical coordinates of the vector head as a list
        [r, theta, z]
    toSpherical : units, optional
        Returns the spherical coordinates of the vector head as a list
        [r, theta, phi]
    unit :
        Return the vector as a unit vector
        
    """

    def __init__(self, head, tail = []):
        
        if isinstance(head, __class__):
            if head._dim != 3:
                raise Exception("Vector3D can only be initialized with a two-dimensional vector.")
            else:
                self._head = head._head.copy()
                self._tail = head._tail.copy()
                self._dim = head._dim
                self._dtype = head._dtype
                self._origin = head._origin.copy()
                self._component = head._component.copy()
                self._norm = head._norm
                return
        else:
            try:
                _ = list(head)
            except TypeError:
                raise TypeError("Expected list or similar castable object as vector. Got " + str(type(head)) + ".")
            except:
                raise Exception("Unknown error in class constructor.")
            if len(list(head)) != 3:
                raise Exception("Vector3D can only be initialized with a two-dimensional list.")
                
        super().__init__(head, tail)
        
    @property            
    def x(self):
        return self._head[0]
    
    @property
    def y(self):
        return self._head[1]
    
    @property
    def z(self):
        return self._head[2]
        
    def _checkTypeCompatability(self, other):
        """
        A type check to make sure that operations between vectors are specified
        using the SimpleVector class or Vector2D clas and that they share both
        dimension.
        """
        if not isinstance(other, __class__):
            raise TypeError("Both arguments must be of the Vector2D class.")
        if other.dim != 3:
            raise Exception("Vectors are of unequal dimension.")
    
    def angle(self, other, units = "rad"):
        """
        Returns the angle between two 3-dimensional vectors.
        
        Parameters
        ----------
        other : vector
            The vector with which to find the angle
            
        Returns
        -------
        float
            The angle in either radians or degrees
            
        """
        
        self._checkTypeCompatability(other)
        if units not in ["rad", "radians", "deg", "degrees"]:
            raise Exception('Units must be "rad" or "deg" for radians or degrees.')
        else:
            units = units[:3]
        sineTheta = self.cross(other).norm / (self.norm * other.norm)
        result = asin(sineTheta)
        if units == "deg":
            result = result * 180 / pi
        return result
    
    def cross(self, other):
        """
        Returns the cross product of the two vectors
        
        Parameters
        ----------
        other : vector
            The vector with which we will compute the cross product. Note that
            the cross product willl be taken in the direction of other
            (right-hand rule).
        
        Returns
        -------
        vector
            A Vector3D which is the cross product of the two vectors.
            
        """
        
        self._checkCompatability(other)
        if (self._tail != other._tail):
            raise Exception("Vector tails do not share the same coordinates.")
        comp1 = self._component
        comp2 = other._component
        
        iComp = comp1[1] * comp2[2] - comp1[2] * comp2[1]
        jComp = comp1[0] * comp2[2] - comp1[2] * comp2[0]
        kComp = comp1[0] * comp2[1] - comp1[1] * comp2[0]
        
        cross = Vector3D([iComp, jComp, kComp], tail = [])
        cross = cross.shift(self._tail)
        return cross
    
    def sine(self, other):
        """
        Returns the cosine of the angle between two vectors:
                        |x x y|
            sinTheta = ---------
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
        return self.cross(other).norm / (self.norm * other.norm)
    
    def toCylindrical(self, units = "rad"):
        """
        toCylindrical will return will return the vector in [r, theta, z]
        form, r being the length of the vector, theta being the angle made
        between the vector projected into the xy-plane and the x-axis, and
        z being the actual z-coordinate of the vector. The values r and theta
        will both be positive. Theta will be 0 <= theta, phi < 2 * pi or
        0 <= theta, phi < 360 depending upon the units. If the tail is
        anywhere but the origin, the origin will be reset to (0, 0, 0). If
        the vector is the zero vector, (0, 0, 0) will be returned.
        
        Parameters
        ----------
        units : {'rad', 'radians', 'deg', 'degrees'}
            Specify whether to return the angle in radians or degrees
            
        Returns
        -------
        list
            [r, theta, z]
            
        """
        
        if self[0] == 0 and self[1] == 0 and self[2] == 0:
            return [0, 0, 0]
        if units not in ["rad", "radians", "deg", "degrees"]:
            raise Exception('Units must be "rad" or "deg" for radians or degrees.')
        else:
            units = units[:3]
        tempX = self._component[0]
        tempY = self._component[1]
        tempZ = self._component[2]
        r = sqrt(tempX ** 2 + tempY ** 2)
        
        #First calculate theta by measuring the angle in the vector projection
        #in the xy-plane.
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
        return [r, theta, tempZ]

    def toSpherical(self, units = "rad"):
        """
        toSpherical will return will return the vector in [r, theta, phi]
        form, r being the length of the vector, theta being the angle made
        between the vector projected into the xy-plane and the x-axis, and
        phi being the angle between the projection and the actual vector.
        The values r, theta, and phi will all be positive. Theta and phi
        will be 0 <= theta, phi < 2 * pi or 0 <= theta, phi < 360 depending
        upon the units. If the tail is anywhere but the origin, the origin
        will be reset to (0, 0, 0). If the vector is the zero vector,
        (0, 0, 0) will be returned.
        
        Parameters
        ----------
        units : {'rad', 'radians', 'deg', 'degrees'}
            Specify whether to return the angle in radians or degrees
            
        Returns
        -------
        list
            [r, theta, phi]
            
        """
        
        if self[0] == 0 and self[1] == 0 and self[2] == 0:
            return [0, 0, 0]
        if units not in ["rad", "radians", "deg", "degrees"]:
            raise Exception('Units must be "rad" or "deg" for radians or degrees.')
        else:
            units = units[:3]
        tempX = self._component[0]
        tempY = self._component[1]
        tempZ = self._component[2]
        r = sqrt(tempX ** 2 + tempY ** 2 + tempZ ** 2)
        
        #First calculate theta by measuring the angle in the vector projection
        #in the xy-plane.
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
        
        #Now we calculate phi as arccos(z/sqrt(x**2 + y**2 + z**2)) which
        #we can do more easily since z/sqrt(x**2 + y**2 + z**2) will
        #always be between -1 and 1.
        phi = acos(tempZ/r)
        if units == "deg":
            theta = theta * 180 / pi
            phi = phi * 180 / pi
        return [r, theta, phi]
