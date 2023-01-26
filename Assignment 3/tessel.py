#author: Fouzia Ahsan
#student number: 250972275
#date: March 17th, 2022
#course: cs3388B
#purpose: Program the contructor method for the tessel class so that it can turn the objects into convex polygons and color/shade them in

import numpy as np
from matrix import matrix

class tessel:

    #Constructor Method
    #Initializes the tessel class
    #:param objectList: List of objects in the graphical scene (input parameter)
    #:param camera: The camera viewing system (input parameter)
    #:param light: The light source (input parameter)
    def __init__(self,objectList,camera,light):

        EPSILON = 0.001

        #Create an empty list of faces. This is an instance variable for this class
        self.__faceList = []

        #Create an empty list for the points forming a face
        facePoints = []

        #Transform the position of the light into viewing coordinates
        #(use method worldToViewingCoordinates from class cameraMatrix)
        lightViewingCoord = camera.worldToViewingCoordinates(light.getPosition())

        #Get light intensity values
        lightIntensity = light.getIntensity()

        #For each object in objectList:
        for object in objectList:

            #Get the object color
            objColor = object.getColor()

            #u becomes the start value of the u-parameter range for the object
            u = object.getURange()[0]

            #While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
            while (u + object.getUVDelta()[0]) < (object.getURange()[1] + EPSILON):

                #v become the start value of the v-parameter range for the object
                v = object.getVRange()[0]

                #While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
                while (v + object.getUVDelta()[1]) < (object.getVRange()[1] + EPSILON):

                    #Collect surface points transformed into viewing coordinates in the following way:
                    #Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
                    deltaU = object.getUVDelta()[0]
                    deltaV = object.getUVDelta()[1]

                    p1 = object.getPoint(u,v)
                    p2 = object.getPoint(u, v + deltaV)
                    p3 = object.getPoint(u + deltaU, v + deltaV)
                    p4 = object.getPoint(u + deltaU, v)

                    #Transform these points with the transformation matrix of the object
                    T1 = object.getT()*p1
                    T2 = object.getT()*p2
                    T3 = object.getT()*p3
                    T4 = object.getT()*p4

                    #Transform these points from world to viewing coordinates
                    P1 = camera.worldToViewingCoordinates(T1)
                    P2 = camera.worldToViewingCoordinates(T2)
                    P3 = camera.worldToViewingCoordinates(T3)
                    P4 = camera.worldToViewingCoordinates(T4)

                    #Append these points (respecting the order) to the list of face points
                    facePoints.append(P1)
                    facePoints.append(P2)
                    facePoints.append(P3)
                    facePoints.append(P4)

                    #Make sure we don't render any face with one or more points behind the near plane in the following way:
                    #Compute the minimum Z-coordinate from the face points
                    minZCoord = self.__minCoordinate(facePoints,2)

                    #If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):
                    nearPlane = camera.getNp()

                    if not minZCoord > -(nearPlane):

                        #Compute the centroid point of the face points
                        centPoint = self.__centroid(facePoints)

                        #Compute the normal vector of the face, normalized
                        normVect = self.__vectorNormal(facePoints)

                        #Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
                        #if not backFace(centroid, face normal):
                        if not self.__backFace(centPoint, normVect):

                            #S is the vector from face centroid to light source, normalized
                            S = self.__vectorToLightSource(lightViewingCoord, centPoint)

                            #R is the vector of specular reflection
                            R = self.__vectorSpecular(S, normVect)

                            #V is the vector from the face centroid to the origin of viewing coordinates
                            V = self.__vectorToEye(centPoint)

                            #Compute color index
                            colorIndex = self.__colorIndex(object, normVect, S, R, V)

                            #Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
                            #(object color (red channel) * light intensity (red channel) * index,
                            # object color (green channel) * light intensity (green channel) * index,
                            # object color (blue channel) * light intensity (blue channel) * index)
                            red = int(objColor[0]*lightIntensity[0]*colorIndex)
                            green = int(objColor[1]*lightIntensity[1]*colorIndex)
                            blue = int(objColor[2]*lightIntensity[2]*colorIndex)

                            faceColor = (red, green, blue)

                            pixelFacePoint = []
                            #For each face point:
                            for point in facePoints:

                                #Transform point into 2D pixel coordinates and append to a pixel face point list
                                pixelFacePoint.append(camera.viewingToPixelCoordinates(point))

                            #Add all face attributes to the list of faces in the following manner:
                            #transform the face centroid from viewing to pixel coordinates
                            pixelFaceCent = camera.viewingToPixelCoordinates(centPoint)

                            #append pixel Z-coordinate of face centroid, the pixel face point list, and the face color
                            self.__faceList.append((pixelFaceCent.get(2,0),pixelFacePoint,faceColor))

                    #Re-initialize the list of face points to empty
                    facePoints = []

                    #v become v + delta v
                    v = v + object.getUVDelta()[1]

                #u becomes u + delta u
                u = u + object.getUVDelta()[0]

    def __minCoordinate(self,facePoints,coord):
	#Computes the minimum X, Y, or Z coordinate from a list of 3D points
	#Coord = 0 indicates minimum X coord, 1 indicates minimum Y coord, 2 indicates minimum Z coord.
        min = facePoints[0].get(coord,0)
        for point in facePoints:
            if point.get(coord,0) < min:
                min = point.get(coord,0)
        return min

    def __backFace(self,C,N):
	#Computes if a face is a back face with using the dot product of the face centroid with the face normal vector
        return C.dotProduct(N) > 0.0

    def __centroid(self,facePoints):
	#Computes the centroid point of a face by averaging the points of the face
        sum = matrix(np.zeros((4,1)))
        for point in facePoints:
            sum += point
        return sum.scalarMultiply(1.0/float(len(facePoints)))

    def __vectorNormal(self,facePoints):
	#Computes the normalized vector normal to a face with the cross product
        U = (facePoints[3] - facePoints[1]).removeRow(3).normalize()
        V = (facePoints[2] - facePoints[0]).removeRow(3).normalize()
        return U.crossProduct(V).normalize().insertRow(3,0.0)

    def __vectorToLightSource(self,L,C):
        return (L.removeRow(3) - C.removeRow(3)).normalize().insertRow(3,0.0)

    def __vectorSpecular(self,S,N):
        return  S.scalarMultiply(-1.0) + N.scalarMultiply(2.0*(S.dotProduct(N)))

    def __vectorToEye(self,C):
        return C.removeRow(3).scalarMultiply(-1.0).normalize().insertRow(3,0.0)

    def __colorIndex(self,object,N,S,R,V):
	#Computes local components of shading
        Id = max(N.dotProduct(S),0.0)
        Is = max(R.dotProduct(V),0.0)
        r = object.getReflectance()
        index = r[0] + r[1]*Id + r[2]*Is**r[3]
        return index

    def getFaceList(self):
        return self.__faceList
