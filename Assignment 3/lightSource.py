#author: Fouzia Ahsan
#student number: 250972275
#date: March 17th, 2022
#course: cs3388B
#purpose: Program the methods for the light source

import numpy as np
from matrix import matrix

class lightSource:

    #Constructor Method
    #Initializes the light source
    #:param position: The position of the light source (input parameter)
    #:param color: The color of the light source (input parameter)
    #:param intensity: The intensity of the light source (input parameter)
    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    #getPosition Method
    #Gets the position of the light source
    #:return: __position
    def getPosition(self):
        return self.__position

    #getColor Method
    #Gets the color of the light
    #:return: __color
    def getColor(self):
        return self.__color

    #getIntensity Method
    #Gets the intensity of the light source
    #:return: __intensity
    def getIntensity(self):
        return  self.__intensity

    #setPosition Method
    #Sets the position of the light source
    #:param position: position of the light source (input parameter)
    def setPosition(self,position):
        self.__position = position

    #setColor Method
    #Sets the color of the light
    #:param color: color of the light source (input parameter)
    def setColor(self,color):
        self.__color = color

    #setIntensity Method
    #Sets the intensity of the light source
    #:param intensity: intensity of the light source (input parameter)
    def setIntensity(self,intensity):
        self.__intensity = intensity
