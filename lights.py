from MathLib import *


class Light(object):
    def __init__(self, color=[1, 1, 1], intensity=1.0, lighType="None"):
        self.color = color
        self.intensity = intensity
        self.lighType = lighType

    def GetLightColor(self, intercept=None):
        return [(i * self.intensity) for i in self.color]

    def GetSpecularColor(self, intercept, viewPos):
        return [0, 0, 0]


class AmbientLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0):
        super().__init__(color, intensity, "Ambient")


class DirectionalLight(Light):
    def __init__(self, color=[1, 1, 1], intensity=1.0, direction=[0, -1, 0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalize_vector(direction)

    def GetLightColor(self, intercept=None):
        lightColor = super().GetLightColor()
        if intercept:
            dir = [(i * -1) for i in self.direction]
            intensity = dot(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor

    def GetSpecularColor(self, intercept, viewPos):
        specColor = self.color

        if intercept:
            dir = [(i * -1) for i in self.direction]
            reflect = calc_reflection(intercept.normal, dir)

            viewDir = sub_elements(viewPos, intercept.point)
            viewDir = normalize_vector(viewDir)

            specularity = max(0, dot(viewDir, reflect) ** intercept.obj.material.spec)
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            specColor = [(i * specularity) for i in specColor]

        return specColor