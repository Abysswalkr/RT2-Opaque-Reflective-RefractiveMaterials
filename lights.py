from MathLib import *

class Illumination(object):
    def __init__(self, lightColor=[1, 1, 1], brightness=1.0, lightCategory="None"):
        self.lightColor = lightColor
        self.brightness = brightness
        self.lightCategory = lightCategory

    def calculateLightIntensity(self, hitPoint=None):
        return [(c * self.brightness) for c in self.lightColor]

    def calculateSpecularHighlight(self, hitPoint, observerPosition):
        return [0, 0, 0]

class BackgroundLight(Illumination):
    def __init__(self, lightColor=[1, 1, 1], brightness=1.0):
        super().__init__(lightColor, brightness, "Ambient")

class Sunlight(Illumination):
    def __init__(self, lightColor=[1, 1, 1], brightness=1.0, directionVector=[0, -1, 0]):
        super().__init__(lightColor, brightness, "Directional")
        self.directionVector = normalize_vector(directionVector)

    def calculateLightIntensity(self, hitPoint=None):
        baseLightColor = super().calculateLightIntensity()
        if hitPoint:
            inverseDirection = [(-d) for d in self.directionVector]
            lightStrength = dot(hitPoint.normal, inverseDirection)
            lightStrength = max(0, min(1, lightStrength))
            lightStrength *= (1 - hitPoint.obj.propiedadesMaterial.reflectivity)  # Cambiado 'material' a 'propiedadesMaterial'
            baseLightColor = [(c * lightStrength) for c in baseLightColor]
        return baseLightColor

    def calculateSpecularHighlight(self, hitPoint, observerPosition):
        specularHighlight = self.lightColor

        if hitPoint:
            inverseDirection = [(-d) for d in self.directionVector]
            reflectedRay = calcularReflejo(hitPoint.normal, inverseDirection)

            viewDirection = restar_elementos(observerPosition, hitPoint.point)
            viewDirection = normalize_vector(viewDirection)

            specularFactor = max(0, dot(viewDirection, reflectedRay) ** hitPoint.obj.propiedadesMaterial.shininess)  # Cambiado 'material' a 'propiedadesMaterial'
            specularFactor *= hitPoint.obj.propiedadesMaterial.reflectivity
            specularFactor *= self.brightness
            specularHighlight = [(c * specularFactor) for c in specularHighlight]

        return specularHighlight
