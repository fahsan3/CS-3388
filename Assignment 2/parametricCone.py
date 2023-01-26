#author: Fouzia Ahsan
#student number: 250972275
#date: February 17th, 2022
#course: cs3388B
#purpose: Program the methods to create a cone for the parametricCone class

from math import *
import numpy as np
from matrix import matrix
from parametricObject import parametricObject

class parametricCone(parametricObject):
    
    #Constructor Method
    #Initializes the parametricCone
    #:param T: The transformation matrix for the cone (input parameter)
    #:param height: The height of the cone (input parameter)
    #:param radius: The radius of the cone (input parameter)
    #:param color: The color of the cone (input parameter)
    #:param reflectance: (input parameter)
    #:param uRange: (input parameter)
    #:param vRange: (input parameter)
    #:param uvDelta: (input parameter)
    #(Copying the constructor method from parametricSphere)
    def __init__(self,T=matrix(np.identity(4)),height=1.0,radius=1.0,color=(255,255,255),reflectance=(0.2,0.4,0.4,1.0),uRange=(0.0,pi),vRange=(0.0,2.0*pi),uvDelta=(pi/18.0,pi/18.0)):
        super().__init__(T,color,reflectance,uRange,vRange,uvDelta)
        self.__height = height
        self.__radius = radius
    
    #getPoint
    #Gets the 3 dimensional points for the cone mesh
    #:param u: The u vector (input parameter)
    #:param v: The v vector (input parameter)
    #:return: P
    def getPoint(self,u,v):

        #According to Lecture 7, Slide 12, the equation for a cone is
        #            |  ((h*(1-u))/h)*r*sin(v)  |
        #   p(u,v) = |  ((h*(1-u))/h)*r*cos(v)  |
        #            |            hu            |
        #            |            1             |

        #If we start with a column matrix of only ones, we would only need to change the values of the first, second and third rows

        #Create a 4x1 matrix of ones to store the points
        P = matrix(np.ones((4,1)))

        #Get the radius and height
        r = self.__radius
        h = self.__height

        #Calculate the expression with h
        hCalc = (h*(1-u))/h

        #Calculate what's in the first row (X(u,v))
        Xuv = hCalc*r*(sin(v))

        #Calculate what's in the first row (Y(u,v))
        Yuv = hCalc*r*(cos(v))

        #Set the value for the first row
        P.set(0,0,Xuv)

        #Set the value for the seoond row
        P.set(1,0,Yuv)

        #Set the value for the third row
        P.set(2,0,(h*u))

        #Return the value of P
        return P

    #Setter Methods

    #setHeight Method
    #Sets the height of the cone
    #:param height: height of the cone (input parameter)
    def setHeight(self,height):
        self.__height = height

    #setRadius Method
    #Sets the radius of the cone
    #:param radius: radius of the cone (input parameter)
    def setRadius(self,radius):
        self.__radius = radius

    #Getter Methods

    #getHeight Method
    #Gets the height of the cone
    #:return: height
    def getHeight(self):
        return self.__height

    #getRadius Method
    #Gets the radius of the cone
    #:return: radius
    def getRadius(self):
        return self.__radius
