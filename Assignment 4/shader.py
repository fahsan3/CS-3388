#author: Fouzia Ahsan
#student number: 250972275
#date: April 7th, 2022
#course: cs3388B
#purpose: Program the constructor and helper method for class shader

class shader:

    #Helper Method (__shadowed)
    #This method checks if the ray from the intersection point to the light source intersects with an object
    #(i.e. this method checks if there should a shadow at a specific intersection point)
    #:param object: Object that there is an intersection with (input parameter)
    #:param I: The intersection point (input parameter)
    #:param S: The vector to the light source (input parameter)
    #:param objectList: The list of objects composing the scene (input parameter)
    #:return: true if the ray from the intersection point to the light source intersects with an object; false otherwise
    def __shadowed(self,object,I,S,objectList):

        #Using the algorithm for the helper method __shadowed given in Lecture 13: Ray Tracing Initial Algorithms (pg.4)

        #M = matrix T associated with object
        M = object.getT()

        #compute I=M*(I+ϵS) where ϵ=0.001
        e = 0.001
        I = M*(I + (S.scalarMultiply(e)))

        #compute S=MS
        S = M*S

        #for object in objectList:
        for obj in objectList:

            #M^−1 = inverse of matrix T associated with object
            matrixT = obj.getT()
            inverseM = matrixT.inverse()

            #compute I=(M^−1)*I
            newI = inverseM*I

            #compute S=(M^−1)S
            newS = inverseM*S

            #normalize S
            newS = newS.normalize()

            #if object.intersection (I ,S) ≠ −1.0 :
            if obj.intersection(newI,newS) != -1.0:
                #then return True
                return True

        #return false
        return False

    #Constructor Method
    #Initializes the shader
    #:param intersection: The first (k ,t0) tuple from the intersection list (input parameter)
    #:param direction: The vector describing the direction of the ray (input parameter)
    #:param camera: The camera matrix (input parameter)
    #:param objectList: The list of objects composing the scene (input parameter)
    #:param light: The lightSource object (input parameter)
    def __init__(self,intersection,direction,camera,objectList,light):

        #Using the algorithm for the shader constructer given in Lecture 13: Ray Tracing Initial Algorithms (pg.2-3)

        #consider tuple (k ,t0) from intersection
        #object = objectList [k]
        k = intersection[0]
        object = objectList[k]

        #t0 is the t-value associated with object from tuple (k ,t0)
        t0 = intersection[1]

        #(M^−1) = inverse of matrix T associated with object
        objMatrixT = object.getT()
        inverseM = objMatrixT.inverse()

        #Ts = light position transformed with (M^−1)
        Ts = inverseM*light.getPosition()

        #transform the ray with (M^−1) in the following way:
        #Te = (M^−1)*e , where e is the position of the camera
        e = camera.getE()
        Te = inverseM*e

        #Td = (M^−1)*d , where d is the direction of the ray
        Td = inverseM*direction

        #compute the intersection point as I=Te + Td*t0
        I = Te + (Td.scalarMultiply(t0))

        #compute vector from intersection point to light source position as S=(Ts − I)
        S = (Ts-I)

        #normalize it
        S = S.normalize()

        #compute normal vector at intersection point as N = object.normalVector (I)
        N = object.normalVector(I)

        #compute specular reflection vector as R=−S + (2S⋅N)*N
        SNdotPro = S.dotProduct(N)
        R = N.scalarMultiply(2 * SNdotPro) - S

        #compute vector to center of projection V =Te − I
        V = Te-I

        #normalize it
        V = V.normalize()

        #compute Id = max{N⋅S ,0}
        NSdotPro = N.dotProduct(S)
        Id = max(NSdotPro, 0)

        #compute Is = max{R⋅V ,0}
        RVdotPro = R.dotProduct(V)
        Is = max(RVdotPro, 0)

        #r= object.getReflectance()
        r = object.getReflectance()

        #c = object.getColor()
        c = object.getColor()

        #Li = light.getIntensity()
        Li = light.getIntensity()

        #if the intersection point is not shadowed by other objects
        if self.__shadowed(object,I,S,objectList) != True:

            #compute f =r[0] + r[1]*Id + r[2]*Is**(r[3])
            f = r[0]+ r[1]*Id + r[2]*(Is**(r[3]))

        #else
        else:
            #compute f =r[0]
            f = r[0]

        #compute tuple self.__color = (c[0]*Li[0]*f ,c[1]*Li[1]*f ,c[2]*Li[2]*f )
        color1 = int(c[0]*Li[0]*f)
        color2 = int(c[1]*Li[1]*f)
        color3 = int(c[2]*Li[2]*f)

        self.__color = (color1, color2, color3)


    def getShade(self):
        return self.__color
