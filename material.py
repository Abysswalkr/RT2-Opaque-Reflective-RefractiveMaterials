class SurfaceProperties(object):
    def __init__(self, baseColor, shininess=1.0, reflectivity=0.0):
        self.baseColor = baseColor
        self.shininess = shininess
        self.reflectivity = reflectivity

    def computeColor(self, intersection, scene):

        totalLight = [0, 0, 0]
        surfaceColor = self.baseColor

        for illumination in scene.lights:
            occlusion = None

            if illumination.lightCategory == "Directional":
                directionToLight = [-d for d in illumination.directionVector]
                occlusion = scene.lanzarRayo(intersection.point, directionToLight, intersection.obj)

            if occlusion is None:
                directLightColor = illumination.calculateLightIntensity(intersection)
                highlightColor = illumination.calculateSpecularHighlight(intersection, scene.camera.translate)
                totalLight = [(totalLight[i] + directLightColor[i] + highlightColor[i]) for i in range(3)]

        surfaceColor = [(surfaceColor[i] * totalLight[i]) for i in range(3)]
        surfaceColor = [min(1, surfaceColor[i]) for i in range(3)]
        return surfaceColor
