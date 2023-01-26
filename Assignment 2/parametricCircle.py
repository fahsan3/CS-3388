#author: Fouzia Ahsan
#student number: 250972275
#date: February 17th, 2022
#course: cs3388B
#purpose: Program the methods to create a cicle for the parametricCircle class

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCircle(parametricObject):

    #Constructor Method
    #Initializes the parametricCircle
    #:param T: The transformation matrix for the circle (input parameter)
    #:param radius: The radius of the circle (input parameter)
    #:param color: The color of the circle (input parameter)
    #:param reflectance: (input parameter)
    #:param uRange: (input parameter)
    #:param vRange: (input parameter)
    #:param uvDelta: (input parameter)
    #(Copying the constructor method from parametricSphere)
    def __init__(self,T=matrix(np.identity(4)),radius=1.0,color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,pi),vRange=(0.0,2.0*pi),uvDelta=(pi/18.0,pi/18.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__radius = radius

    #getPoint
    #Gets the 3 dimensional points for the circle mesh
    #:param u: The u vector (input parameter)
    #:param v: The v vector (input parameter)
    #:return: P
    def getPoint(self,u,v):

        #According to Lecture 7, Slide 14, the equation for a circle is
        #            |  rucos(v)  |
        #   p(u,v) = |  rusin(v)  |
        #            |     0      |
        #            |     1      |

        #If we start with a column matrix of only ones, we would only need to change the values of the first, second and third rows

        #Create a 4x1 matrix of ones to store the points
        P = matrix(np.ones((4,1)))

        #Get the radius
        r = self.__radius

        #Calculate what's in the first row (X(u,v))
        Xuv = r*u*(cos(v))

        #Calculate what's in the first row (Y(u,v))
        Yuv = r*u*(sin(v))

        #Set the value for the first row
        P.set(0,0,Xuv)

        #Set the value for the second row
        P.set(1,0,Yuv)

        #Set the value for the third row
        P.set(2,0,0)

        #Return the value of P
        return P

    #Setter Method

    #setRadius Method
    #Sets the radius of the circle
    #:param radius: radius of the circle (input parameter)
    def setRadius(self,radius):
        self.__radius = radius

    #Getter Method

    #getRadius Method
    #Gets the radius of the circle
    #:return: radius
    def getRadius(self):
        return self.__radius
