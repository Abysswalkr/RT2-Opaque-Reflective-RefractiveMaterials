from gl import *
from refracctionFunctions import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

# Producto punto entre dos vectores
def dot_product(v1, v2):
    return sum(v1[i] * v2[i] for i in range(len(v1)))

# Suma de vectores
def vector_add(v1, v2):
    return [v1[i] + v2[i] for i in range(len(v1))]

# Resta de vectores
def vector_subtract(v1, v2):
    return [v1[i] - v2[i] for i in range(len(v1))]

# Multiplicación escalar-vector
def scalar_multiply(scalar, v):
    return [scalar * comp for comp in v]

class Material(object):
    def __init__(self, difuse=[1,1,1], spec=1.0, Ks=0.0, ior=1.0, matType=OPAQUE, texture=None):
        self.difuse = difuse
        self.spec = spec
        self.Ks = Ks
        self.matType = matType
        self.texture = texture
        self.ior = ior

    def GetSurfaceColor(self, intercept, renderer, recursion=0):
        # phong reflection model
        # LightColors = LightColor + Specular
        # FinalColor = DiffuseColor * LightColor

        lightColor = [0, 0, 0]
        reflectColor = [0, 0, 0]
        finalColor = self.difuse
        refractColor = [0, 0, 0]

        if self.texture and intercept.texCoords:
            textureColor = self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [finalColor[i] * textureColor[i] for i in range(3)]

        for light in renderer.lights:
            shadowIntercept = None

            if light.lighType == "Directional":
                lightDir = [-i for i in light.direction]
                shadowIntercept = renderer.glCastRay(intercept.point, lightDir, intercept.obj)

            if shadowIntercept is None:
                lightColor = [(lightColor[i] + light.GetSpecularColor(intercept, renderer.camera.translate)[i]) for i in range(3)]
                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]

        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = calc_reflection(intercept.normal, rayDir)
            reflectIntercept = renderer.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept is not None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

        elif self.matType == TRANSPARENT:
            # Se revisa si estamos afuera
            outside = dot_product(intercept.normal, intercept.rayDirection) < 0

            # Agregar margen de error
            bias = scalar_multiply(0.001, intercept.normal)

            # Generar rayos de reflexión
            rayDir = [-i for i in intercept.rayDirection]
            reflect = calc_reflection(intercept.normal, rayDir)
            reflectOrig = vector_add(intercept.point, bias) if outside else vector_subtract(intercept.point, bias)
            reflectIntercept = renderer.glCastRay(reflectOrig, reflect, None, recursion + 1)
            if reflectIntercept is not None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, renderer, recursion + 1)
            else:
                reflectColor = renderer.glEnvMapColor(intercept.point, reflect)

            # Generar los rayos de refracción
            if not totalInternalReflection(intercept.normal, intercept.rayDirection, 1.0, self.ior):
                refract = refractVector(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                refractOrig = vector_subtract(intercept.point, bias) if outside else vector_add(intercept.point, bias)
                refractIntercept = renderer.glCastRay(refractOrig, refract, None, recursion + 1)
                if refractIntercept is not None:
                    refractColor = refractIntercept.obj.material.GetSurfaceColor(refractIntercept, renderer, recursion + 1)
                else:
                    refractColor = renderer.glEnvMapColor(intercept.point, refract)

                # Usando las ecuaciones de Fresnel, determinamos cuánta reflexión y cuánta refracción agregar al color final
                Kr, Kt = fresnel(intercept.normal, intercept.rayDirection, 1.0, self.ior)
                reflectColor = [i * Kr for i in reflectColor]
                refractColor = [i * Kt for i in refractColor]

        finalColor = [(finalColor[i] * (lightColor[i] + reflectColor[i] + refractColor[i])) for i in range(3)]
        finalColor = [min(1, finalColor[i]) for i in range(3)]

        return finalColor
