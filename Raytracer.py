import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import SurfaceProperties
from lights import *

# Configuración de pantalla
width = 540
height = 540

screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

# Inicialización del renderizador
rt = RendererRT(screen)

# Definición de materiales
ladrillo = SurfaceProperties(baseColor=[1, 0.2, 0.2], shininess=128, reflectivity=0.25)
cesped = SurfaceProperties(baseColor=[0.2, 1.0, 0.2], shininess=64, reflectivity=0.2)

nieve = SurfaceProperties(
    baseColor=[0.95, 0.95, 0.95],
    shininess=128,
    reflectivity=0.3
)

boton = SurfaceProperties(
    baseColor=[0.09, 0.09, 0.09],  # Gris muy oscuro, casi negro
    shininess=32,                   # Exponente especular bajo para un reflejo suave
    reflectivity=0.1                # Bajo coeficiente especular para un acabado mate
)

zanahoria_naranja = SurfaceProperties(
    baseColor=[1.0, 0.5, 0.0],
    shininess=32,
    reflectivity=0.2
)

# Iluminación de la escena
rt.lights.append(Sunlight(directionVector=[0, 1, 0], brightness=0.8))  # Luz desde abajo hacia arriba
rt.lights.append(Sunlight(directionVector=[0.5, 1, -1], brightness=0.8, lightColor=[1, 1, 1]))  # Otra luz desde un ángulo
rt.lights.append(BackgroundLight(brightness=0.1))  # Luz ambiental débil

# Creación de las figuras geométricas en la escena
rt.scene.append(Esfera(centro=[0, 0.6, -2.8], radio=0.3, propiedadesMaterial=nieve))  # Cabeza
rt.scene.append(Esfera(centro=[0, 0.5, -2.55], radio=0.06, propiedadesMaterial=zanahoria_naranja))  # Nariz
rt.scene.append(Esfera(centro=[-0.04, 0.44, -2.57], radio=0.025, propiedadesMaterial=boton))  # Boca
rt.scene.append(Esfera(centro=[0.04, 0.44, -2.57], radio=0.025, propiedadesMaterial=boton))   # Boca
rt.scene.append(Esfera(centro=[0.11, 0.46, -2.58], radio=0.025, propiedadesMaterial=boton))   # Boca
rt.scene.append(Esfera(centro=[-0.11, 0.46, -2.58], radio=0.025, propiedadesMaterial=boton))  # Boca

rt.scene.append(Esfera(centro=[-0.09, 0.6, -2.52], radio=0.05, propiedadesMaterial=boton))  # Ojo izquierdo (más grande)
rt.scene.append(Esfera(centro=[0.09, 0.6, -2.52], radio=0.05, propiedadesMaterial=boton))   # Ojo derecho (más grande)

rt.scene.append(Esfera(centro=[0, 0, -2.9], radio=0.4, propiedadesMaterial=nieve))  # Cuerpo medio

# Botones del muñeco de nieve (ajustar posiciones en el eje Y para centrarlos)
rt.scene.append(Esfera(centro=[0, 0.15, -2.58], radio=0.08, propiedadesMaterial=boton))  # Botón superior (más abajo)
rt.scene.append(Esfera(centro=[0, -0.1, -2.53], radio=0.1, propiedadesMaterial=boton))   # Botón medio (más abajo)
rt.scene.append(Esfera(centro=[0, -0.6, -2.6], radio=0.15, propiedadesMaterial=boton))   # Botón inferior (más abajo)

rt.scene.append(Esfera(centro=[0, -0.7, -3], radio=0.5, propiedadesMaterial=nieve))  # Bola inferior

# Renderizado de la escena
rt.glRender()

# Bucle principal de ejecución
isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
