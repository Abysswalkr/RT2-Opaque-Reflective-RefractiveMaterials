from MathLib import calc_reflection
from gl import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Material(object):
    def __init__(self, difuse = [1,1,1], spec=1.0, Ks=0.0, matType=OPAQUE, texture = None):
        self.difuse = difuse
        self.spec = spec
        self.Ks = Ks
        self.matType = matType
        self.texture = texture

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        # phong reflection model
        # LightColors = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor

        lightColor = [0, 0, 0]
        reflectColor = [0, 0, 0]
        finalColor = self.difuse

        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.lights:
            shadowIntercept = None

            if light.lighType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept == None:
                lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in
                              range(3)]
                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]

        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = calc_reflection(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

        finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i])) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]

        return finalColor
