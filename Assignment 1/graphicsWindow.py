#author: Fouzia Ahsan
#student number: 250972275
#date: January 28th, 2021
#course: cs3388B
#purpose: complete class graphicsWindows by finishing method drawLine

import operator
from PIL import Image
import numpy as np

class graphicsWindow:

    def __init__(self,width=640,height=480):
        self.__mode = 'RGB'
        self.__width = width
        self.__height = height
        self.__canvas = Image.new(self.__mode,(self.__width,self.__height))
        self.__image = self.__canvas.load()

    def drawPoint(self,point,color):
        if 0 <= point[0] < self.__width and 0 <= point[1] < self.__height:
            self.__image[point[0],point[1]] = color

    def drawLine(self,point1,point2,color):

        #Get the x and y coordinates
        #Point1 = (x1, y1)
        x1=point1.get(0,0)
        y1=point1.get(1,0)

        #Point2 = (x2, y2)
        x2=point2.get(0,0)
        y2=point2.get(1,0)

        #Change in x and y [Only going to be used for comparisons not calculations]
        dx = x2 - x1 #Change in x (dx)
        dy = y2 - y1 #Change in y (dy)

        #Slope
        if (dx != 0): #To stop from getting an undefined number (since dividing by zero = undefined)
            slope = dy/dx

        #There are three slope cases to consider when covering all possible slopes:
        #Case 1: |slope| > 1 (covers cases when slope is > 1 and when slope is < -1)
        #Case 2: 0 < |slope| < 1 (covers cases when slope > 0 and < 1 and when slope is > -1 and < 0)
        #Case 3: slope = 0 (horizontal line) and slope = undefined (close to vertical line)

        #Case 1 happens when |dy| > |dx|
        #Case 2 happens when |dy| < |dx|
        #Case 3 happens when dy = 0 (horizontal line) or when dx = 0 (vertical line)

        #When going through the cases, go from smallest case size/simplest restrictions to largest
        #So Case 3 first (slope of 0 or undefined) then Case 2 and everything after that will be Case 1

        #Case 3 (when slope = 0 or slope = undefined (i.e. slope is a vertical line))
        if (dy == 0) or (dx == 0): #since slope = dy/dx, if dy = 0, slope = 0 while if dx = 0, slope = undefined

            if dx == 0: #slope is undefined (will look close to a vertical line)

                if dy < 0: #if dy is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                x = x1

                #plot line up y-axis (i.e. vertical line)
                for y in range(np.intc(y1),np.intc(y2)):
                    self.drawPoint((x,y),color)

            elif dy == 0: #slope = 0 (will be a horizontal line

                if dx < 0: #if dx is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                y = y1

                #plot line down x-axis (i.e. horizontal line)
                for x in range(np.intc(x1),np.intc(x2)):
                    self.drawPoint((x,y),color)

        #Case 2 ( 0 < |slope| < 1)
        elif (abs(dy) < abs(dx)): #since slope = dy/dx, if |dy| < |dx|, it means 0 < |slope| < 1

            if( slope > 0): #checks if slope is positive (i.e. if 0 < slope < 1)

                if (dy < 0): #if dy is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                #Change in x and y [Used for the calculations for Bresenham's Integer Line Drawing Algorithm]
                dxi = x2 - x1
                dyi = y2 - y1

                #Bresenham's Integer Line Drawing Algorithm for when 0 < slope < 1 (adapted from lecture 2 slides)
                y = y1

                #for (i = x1 to x2, i++) [i = x]
                for x in range(np.intc(x1),np.intc(x2)):

                    #if (i == x1)
                    if (x == x1):

                        #pi = 2*dy - dx
                        pi = (2*dyi) - dxi

                    #else
                    else:

                        #if (pi < 0)
                        if pi < 0:

                            #pi = pi + 2*dy
                            pi = pi + (2*dyi)

                        #else
                        else:

                            #pi = pi + 2*dy - 2*dx
                            pi = pi + (2*(dyi - dxi))

                            #y++
                            y = y + 1

                    #plot(x1,y1)
                    self.drawPoint((x,y),color)

            elif (slope < 0): #checks if slope is negative (i.e. if -1 < slope < 0)

                if dy > 0 and dx < 0: #if dy is positive & dx is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                #Change in x and y [Used for the calculations for Bresenham's Integer Line Drawing Algorithm]
                dxi = x2 - x1
                dyi = y1 - y2

                #Bresenham's Integer Line Drawing Algorithm for when -1 < slope < 0 (adapted from lecture 2 slides)
                y = y1

                #for (i = x1 to x2, i++) [i = x]
                for x in range(np.intc(x1),np.intc(x2)):

                    #if (i == x1)
                    if (x == x1):

                        #pi = 2*dy - dx
                        pi = (2*dyi) - dxi

                    #else
                    else:

                        #if (pi < 0)
                        if pi < 0:

                            #pi = pi + 2*dy
                            pi = pi + (2*dyi)

                        #else
                        else:

                            #pi = pi + 2*dy - 2*dx
                            pi = pi + (2*(dyi - dxi))

                            #y--
                            y = y - 1 #slope is negative so have to subtract 1 from y

                    #plot(x1,y1)
                    self.drawPoint((x,y),color)

        #Case 1 (|slope| > 1) [i.e. any slope that isn't 0, undefined or between -1 and 1]
        else:

            if slope > 0: #checks if slope is positive (i.e. if slope > 1)

                if dx < 0: #if dx is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                #Change in x and y [Used for the calculations for Bresenham's Integer Line Drawing Algorithm]
                dxi = x2 - x1
                dyi = y2 - y1

                #Bresenham's Integer Line Drawing Algorithm for when slope > 1 (adapted from lecture 2 slides)
                #[x and y are exchanged in this case]

                x = x1

                #for (i = x1 to x2, i++) [i = y, and x1 and x2 are substituted for y1 and y2 respectively]
                for y in range(np.intc(y1),np.intc(y2)):

                    #if (i == x1)
                    if y == y1:

                        #pi = 2*dy - dx
                        pi = (2*dxi) - dyi

                    #else
                    else:

                        #if (pi < 0)
                        if pi < 0:

                            #pi = pi + 2*dy
                            pi = pi + (2*dxi)

                        #else
                        else:

                            #pi = pi + 2*dy - 2*dx
                            pi = pi + (2*(dxi - dyi))

                            #y++
                            x = x + 1

                    #plot(x1,y1)
                    self.drawPoint((x,y),color)

            elif (slope < 0): #checks if slope is negative (i.e. if slope < -1)

                if dy < 0: #if dx is negative, have to swap the values of (x1,y1) and (x2,y2)
                    x1,x2 = x2,x1 #swapping x values
                    y1,y2 = y2,y1 #swapping y values

                #Change in x and y [Used for the calculations for Bresenham's Integer Line Drawing Algorithm]
                dxi = x1 - x2
                dyi = y2 - y1

                #Bresenham's Integer Line Drawing Algorithm for when slope < -1 (adapted from lecture 2 slides)
                #[x and y are exchanged in this case]

                x = x1

                #for (i = x1 to x2, i++) [i = y, and x1 and x2 are substituted for y1 and y2 respectively]
                for y in range(np.intc(y1),np.intc(y2)):

                    #if (i == x1)
                    if y == y1:

                        #pi = 2*dy - dx
                        pi = (2*dxi) - dyi

                    #else
                    else:

                        #if (pi < 0)
                        if pi < 0:

                            #pi = pi + 2*dy
                            pi = pi + (2*dxi)

                        #else
                        else:

                            #pi = pi + 2*dy - 2*dx
                            pi = pi + (2*(dxi - dyi))

                            #y--
                            x = x - 1 #slope is negative so have to subtract 1 from x

                    #plot(x1,y1)
                    self.drawPoint((x,y),color)

    def saveImage(self,fileName):
        self.__canvas.save(fileName)

    def showImage(self):
        self.__canvas.show()

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height
