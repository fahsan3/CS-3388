#author: Fouzia Ahsan
#student number: 250972275
#date: February 17th, 2022
#course: cs3388B
#purpose: Program the helper methods (setMv, setMp, setS1, setS2, setT1, setT2, and setW2) for class cameraMatrix

#import operator
from math import *
import numpy as np
from matrix import matrix

class cameraMatrix:


    #Constructor Method
    #Initializes the cameraMatrix
    #:param window: Dimensions of the screen window for the camera (input parameter)
    #:param UP: Up direction vector (input parameter)
    #:param E: Position of the origin of the camera coordinate system (input parameter)
    #:param G: Gaze point (input parameter)
    #:param nearPlane: Near plane of the viewing volume (input parameter)
    #:param farPlane: Far plane of the viewing volume (input parameter)
    #:param theta: Viewing angle (input parameter)
    def __init__(self,window,UP,E,G,nearPlane=10.0,farPlane=50.0,theta=90.0):

        self.__UP = UP.normalize()
        self.__E = E
        self.__G = G
        self.__np = nearPlane
        self.__fp = farPlane
        self.__width = window.getWidth()
        self.__height = window.getHeight()
        self.__theta = theta
        self.__aspect = self.__width/self.__height
        self.__npHeight = self.__np*(pi/180.0*self.__theta/2.0)
        self.__npWidth = self.__npHeight*self.__aspect

        Mp = self.__setMp(self.__np,farPlane)
        T1 = self.__setT1(self.__np,self.__theta,self.__aspect)
        S1 = self.__setS1(self.__np,self.__theta,self.__aspect)
        T2 = self.__setT2()
        S2 = self.__setS2(self.__width,self.__height)
        W2 = self.__setW2(self.__height)

        self.__N = (self.__E - self.__G).removeRow(3).normalize()
        self.__U = self.__UP.removeRow(3).crossProduct(self.__N).normalize()
        self.__V = self.__N.crossProduct(self.__U)

        self.__Mv = self.__setMv(self.__U,self.__V,self.__N,self.__E)
        self.__C = W2*S2*T2*S1*T1*Mp
        self.__M = self.__C*self.__Mv

    #setMv Method
    #Sets the values for the Mv matrix
    #:param U: Unit vector u of the coordinate system of the camera (input parameter)
    #:param V: Unit vector v of the coordinate system of the camera (input parameter)
    #:param N: Unit vector n of the coordinate system of the camera (input parameter)
    #:param E: Position of the origin of the camera coordinate system (input parameter)
    #:return: Mv
    def __setMv(self,U,V,N,E):

        #According to Lecture 6, Slide 37, the Mv matrix is:
        #        |  ux  uy  uz  -e.u    |
        #   Mv = |  vx  vy  vz  -e.v    |
        #        |  nx  ny  nz  -e.n    |
        #        |  0   0   0    1      |

        #If we start with an identity matrix, we would only need to change the values of the first, second and third rows

        #Create a matrix to store the result for Mv in (an identity matrix would be easiest)
        Mv = matrix(np.identity(4))

        #Calculate the dot products of e and u, e and v, and e and n for the matrix
        doteu = E.get(0,0)*U.get(0,0) + E.get(1,0)*U.get(1,0) + E.get(2,0)*U.get(2,0) #dot product of e and u
        dotev = E.get(0,0)*V.get(0,0) + E.get(1,0)*V.get(1,0) + E.get(2,0)*V.get(2,0) #dot product of e and v
        doten = E.get(0,0)*N.get(0,0) + E.get(1,0)*N.get(1,0) + E.get(2,0)*N.get(2,0) #dot product of e and n

        #Set the values of the first row
        Mv.set(0,0,U.get(0,0)) #ux
        Mv.set(0,1,U.get(1,0)) #uy
        Mv.set(0,2,U.get(2,0)) #uz
        Mv.set(0,3,-(doteu)) #dot product of e and u

        #Set the values of the second row
        Mv.set(1,0,V.get(0,0)) #vx
        Mv.set(1,1,V.get(1,0)) #vy
        Mv.set(1,2,V.get(2,0)) #vz
        Mv.set(1,3,-(dotev)) #dot product of e and v

        #Set the values of the third row
        Mv.set(2,0,N.get(0,0)) #nx
        Mv.set(2,1,N.get(1,0)) #ny
        Mv.set(2,2,N.get(2,0)) #nz
        Mv.set(2,3,-(doten)) #dot product of e and n

        #Return the Mv matrix
        return Mv

    #setMp Method
    #Sets the values for the Mp matrix
    #:param nearPlane: Near plane of the viewing volume (input parameter)
    #:param farPlane: Far plane of the viewing volume (input parameter)
    #:return: Mp
    def __setMp(self,nearPlane,farPlane):

        #According to Lecture 6, Slide 26, the Mp matrix is:
        #        |  N  0  0  0    |
        #   Mp = |  0  N  0  0    |
        #        |  0  0  a  b    |
        #        |  0  0 -1  0    |

        #If we start with an identity matrix, we would need to change the values of all rows

        #Create a matrix to store the result for Mp in (an identity matrix would be easiest)
        Mp = matrix(np.identity(4))

        #Get the values of N, a and b for the Mp matrix
        #(Using the names of the variables from the slides to make it easier)
        N = nearPlane #Redundant but helps when looking at formulas
        F = farPlane #Redundant but helps when looking at formulas
        a = -((F+N)/(F-N)) #Formula for constant a from Lecture 6, Slide 22
        b = -2*((F*N)/(F-N)) #Formula for constant b from Lecture 6, Slide 22

        #Set the values of first row
        Mp.set(0,0,N)

        #Set the values of the second row
        Mp.set(1,1,N)

        #Set the values of the third row
        Mp.set(2,2,a)
        Mp.set(2,3,b)

        #Set the values of the fourth row
        Mp.set(3,2,-1)
        Mp.set(3,3,0)

        #Return the Mp matrix
        return Mp

    #setT1 Method
    #Sets the values for the T1 matrix
    #:param nearPlane: Near plane of the viewing volume (input parameter)
    #:param theta: Viewing angle (input parameter)
    #:param aspect: Aspect ratio (input parameter)
    #:return: T1
    def __setT1(self,nearPlane,theta,aspect):

        #According to Lecture 6, Slide 40, the T1 matrix is:
        #        |  1  0  0  -(r+l)/2   |
        #   T1 = |  0  1  0  -(t+b)/2   |
        #        |  0  0  1      0      |
        #        |  0  0  0      1      |

        #If we start with an identity matrix, we would only need to change the values of the first and second rows

        #Create a matrix to store the result for T1 in (an identity matrix would be easiest)
        T1 = matrix(np.identity(4))

        #Calculate the values of t, r, b and l for the T1 matrix
        #(Using the names of the variables from the slides to make it easier)
        t = nearPlane*(np.tan((theta/2)*((np.pi)/180)))
        r = aspect*t
        b = -t
        l = -r

        #Calculate the expressions in column 4
        calcRL = -((r+l)/2)
        calcTB = -((t+b)/2)

        #Set the values of the first row
        T1.set(0,3,calcRL)

        #Set the values of the second row
        T1.set(1,3,calcTB)

        #Return the T1 matrix
        return T1

    #setS1 Method
    #Sets the values for the S1 matrix
    #:param nearPlane: Near plane of the viewing volume (input parameter)
    #:param theta: Viewing angle (input parameter)
    #:param aspect: Aspect ratio (input parameter)
    #:return: S1
    def __setS1(self,nearPlane,theta,aspect):

        #According to Lecture 6, Slide 40, the S1 matrix is:
        #        |  2/(r-l)    0     0  0   |
        #   S1 = |    0     2/(r-l)  0  0   |
        #        |    0        0     1  0   |
        #        |    0        0     0  1   |

        #If we start with an identity matrix, we would only need to change the values of the first and second rows

        #Following example from Lecture 10 slides

        #Create a matrix to store the result for S1 in (an identity matrix would be easiest)
        S1 = matrix(np.identity(4))

        #Calculate the values of t, r, b and l for the S1 matrix
        #(Using the names of the variables from the slides to make it easier)
        t = nearPlane*(np.tan((theta/2)*((np.pi)/180)))
        r = aspect*t
        b = -t
        l = -r

        #Set the values of the first row
        S1.set(0,0,(2/(r-l)))

        #Set the values of the second row
        S1.set(1,1,(2/(t-b)))

        #Return the S1 matrix
        return S1

    #setT2 Method
    #Sets the values for the T2 matrix
    #:return: T2
    def __setT2(self):

        #According to Lecture 6, Slide 43, the T2 matrix is:
        #        |  1  0  0  1  |
        #   T2 = |  0  1  0  1  |
        #        |  0  0  1  0  |
        #        |  0  0  0  1  |

        #If we start with an identity matrix, we would only need to change the values of the first and second rows

        #Create a matrix to store the result for T2 in (an identity matrix would be easiest)
        T2 = matrix(np.identity(4))

        #Set the values of the first row
        T2.set(0,3,1)

        #Set the values of the second row
        T2.set(1,3,1)

        #Return the T2 matrix
        return T2

    #setS2 Method
    #Sets the values for the S2 matrix
    #:param width:  Width of the screen window (input parameter)
    #:param height: Height of the screen window (input parameter)
    #:return: S2
    def __setS2(self,width,height):

        #According to Lecture 6, Slide 44, the S2 matrix is:
        #        |  w/2  0   0  0  |
        #   S2 = |  0   h/2  0  0  |
        #        |  0    0   1  0  |
        #        |  0    0   0  1  |

        #If we start with an identity matrix, we would only need to change the values of the first and second rows

        #Create a matrix to store the result for S2 in (an identity matrix would be easiest)
        S2 = matrix(np.identity(4))

        #Renaming width and height to the names of the variables used in the slides to make it easier to remember
        w = width
        h = height

        #Set the values of the first row
        S2.set(0,0,(w/2))

        #Set the values of the second row
        S2.set(1,1,(h/2))

        #Return the S2 matrix
        return S2

    #setW2 Method
    #Sets the values for the W2 matrix
    #:param height: Height of the screen window (input parameter)
    #:return: W2
    def __setW2(self,height):

        #According to Lecture 6, Slide 45, the W2 matrix is:
        #        |  1  0  0  0  |
        #   W2 = |  0 -1  0  h  |
        #        |  0  0  1  0  |
        #        |  0  0  0  1  |

        #If we start with an identity matrix, we would only need to change the values of the second row

        #Create a matrix to store the result for W2 in (an identity matrix would be easiest)
        W2 = matrix(np.identity(4))

        #Renaming height to the names of the variables used in the slides to make it easier to remember
        h = height

        #Set the values of the second row
        W2.set(1,1,-1)
        W2.set(1,3,h)

        #Return the W2 matrix
        return W2

    def worldToViewingCoordinates(self,P):
        return self.__Mv*P

    def worldToImageCoordinates(self,P):
        return self.__M*P

    def worldToPixelCoordinates(self,P):
        return self.__M*P.scalarMultiply(1.0/(self.__M*P).get(3,0))

    def viewingToImageCoordinates(self,P):
        return self.__C*P

    def viewingToPixelCoordinates(self,P):
        return self.__C*P.scalarMultiply(1.0/(self.__C*P).get(3,0))

    def imageToPixelCoordinates(self,P):
        return P.scalarMultiply(1.0/P.get(3,0))

    def getUP(self):
        return self.__UP

    def getU(self):
        return self.__U

    def getV(self):
        return self.__V

    def getN(self):
        return self.__N

    def getE(self):
        return self.__E

    def getG(self):
        return self.__G

    def getMv(self):
        return self.__Mv

    def getC(self):
        return self.__C

    def getM(self):
        return self.__M

    def getNp(self):
        return self.__np

    def getFp(self):
        return self.__fp

    def getTheta(self):
        return self.__theta

    def getAspect(self):
        return self.__aspect

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def getNpHeight(self):
        return self.__npHeight

    def getNpWidth(self):
        return self.__npWidth
