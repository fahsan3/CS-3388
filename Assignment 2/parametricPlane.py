#author: Fouzia Ahsan
#student number: 250972275
#date: February 17th, 2022
#course: cs3388B
#purpose: Program the methods to create a plane for the parametricPlane class

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricPlane(parametricObject):

    #Constructor Method
    #Initializes the parametricPlane
    #:param T: The transformation matrix for the plane (input parameter)
    #:param width: The width of the plane (input parameter)
    #:param length: The length of the plane (input parameter)
    #:param color: The color of the plane (input parameter)
    #:param reflectance: (input parameter)
    #:param uRange: (input parameter)
    #:param vRange: (input parameter)
    #:param uvDelta: (input parameter)
    #(Copying the constructor method from parametricSphere)
    def __init__(self,T=matrix(np.identity(4)),width=1.0,length=1.0,color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,pi),vRange=(0.0,2.0*pi),uvDelta=(pi/18.0,pi/18.0)):

        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__width = width
        self.__length = length

    #getPoint
    #Gets the 3 dimensional points for the plane mesh
    #:param u: The u vector (input parameter)
    #:param v: The v vector (input parameter)
    #:return: P
    def getPoint(self,u,v):

        #According to Lecture 7, Slide 15, the equation for a plane is
        #            |  uw  |
        #   p(u,v) = |  vh  |
        #            |  0   |
        #            |  1   |

        #If we start with a column matrix of only ones, we would only need to change the values of the first, second and third rows

        #Create a 4x1 matrix of ones to store the points
        P = matrix(np.ones((4,1)))

        #Calculate the values that go into the matrix
        uw = u*(self.__width)
        vh = v*(self.__length)

        #Set the value for the first row
        P.set(0,0,uw)

        #Set the value for the second row
        P.set(1,0,vh)

        #Set the value for the third row
        P.set(2,0,0)

        #Return the value of P
        return P

    #Setter Methods

    #setWidth Method
    #Sets the width of the plane
    #:param width: Width of the plane (input parameter)
    def setWidth(self,width):
        self.__width = width

    #setLength Method
    #Sets the length of the plane
    #:param length: length of the plane (input parameter)
    def setLength(self,length):
        self.__length = length

    #Getter Methods

    #getWidth Method
    #Gets the width of the plane
    #:return: width
    def getWidth(self):
        return self.__width

    #getLength Method
    #Gets the length of the plane
    #:return: length
    def getLength(self):
        return self.__length
