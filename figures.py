from intercept import Interception
from MathLib import *


class Geometria(object):
    def __init__(self, centro, propiedadesMaterial):
        self.centro = centro
        self.propiedadesMaterial = propiedadesMaterial
        self.tipoGeometria = "Ninguno"

    def intersectarRayo(self, origen, direccion):
        return None


class Esfera(Geometria):
    def __init__(self, centro, radio, propiedadesMaterial):
        super().__init__(centro, propiedadesMaterial)
        self.radio = radio
        self.tipoGeometria = "Esfera"

    def intersectarRayo(self, origen, direccion):
        vectorDistancia = restar_elementos(self.centro, origen)
        tca = dot(vectorDistancia, direccion)

        distanciaNormCuadrada = sum([componente ** 2 for componente in vectorDistancia])  # ||L||^2
        distanciaProyectadaCuadrada = distanciaNormCuadrada - tca ** 2
        if distanciaProyectadaCuadrada < 0:
            return None  # No hay intersección

        distanciaProyectada = sqrt(distanciaProyectadaCuadrada)

        if distanciaProyectada > self.radio:
            return None

        thc = (self.radio ** 2 - distanciaProyectada ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None

        # Punto de intersección = origen + direccion * t0
        direccionEscalada = [comp * t0 for comp in direccion]  # direccion * t0
        puntoInterseccion = suma_vectores(origen, direccionEscalada)  # origen + (direccion * t0)

        # vectorNormal = (PuntoIntersección - self.centro).normalize()
        diferenciaPuntoCentro = restar_elementos(puntoInterseccion, self.centro)
        vectorNormal = normalize_vector(diferenciaPuntoCentro)

        return Interception(
            point=puntoInterseccion,
            normal=vectorNormal,
            distancia=t0,
            obj=self
        )

