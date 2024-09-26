from intercept import Intercept
from MathLib import *
from math import tan, pi, atan2, acos


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None


class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def rayIntersect(self, origin, direction):
        distance_vect = sub_elements(self.position, origin)
        tca = dot(distance_vect, direction)

        normDistSq = sum([comp ** 2 for comp in distance_vect])  # ||L||^2
        projDistSq = normDistSq - tca ** 2
        if projDistSq < 0:
            return None  # No hay intersección

        projDist = sqrt(projDistSq)

        if projDist > self.radius:
            return None

        thc = (self.radius ** 2 - projDist ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # Punto de intersección = origin + direction * t0
        scaledDir = [comp * t0 for comp in direction]  # direction * t0
        intersectPoint = sum_elements(origin, scaledDir)  # origin + (direction * t0)

        # normalVec = (PuntoIntersección - self.centro).normalize()
        pointDiff = sub_elements(intersectPoint, self.position)
        normalVec = normalize_vector(pointDiff)

        u = 1 - ((atan2(normalVec[2], normalVec[0])) / (2 * pi) + 0.5)
        v = acos(-normalVec[1]) / pi

        return Intercept(point=intersectPoint,
                         normal=normalVec,
                         distance=t0,
                         obj=self,
                         rayDirection=direction,
                         texCoords= [u,v]
                         )

