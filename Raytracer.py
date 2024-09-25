import pygame
from pygame.locals import *
from gl import RendererRT
from figures import *
from material import *
from lights import *
from texture import Texture

# Configuración de pantalla
width =  256
height = 256

screen = pygame.display.set_mode((width, height), pygame.SCALED )
clock = pygame.time.Clock()

rt = RendererRT(screen)
rt.envMap = Texture('Textures/fondo.bmp')

rt.glClearColor(0.5,0.0,0.0)
rt.glClear()

brick = Material(difuse = [1, 0.2, 0.2], spec = 128, Ks = 0.25)
grass = Material(difuse = [0.2, 1.0, 0.2], spec = 64, Ks = 0.2)
mirror = Material(difuse = [0.9,0.9,0.9], spec = 128, Ks = 0.2, matType = REFLECTIVE)
blueMirror = Material(difuse=[0.2,0.2,0.9], spec=128, Ks=0.2, matType=REFLECTIVE)


# Iluminación de la escena
rt.lights.append(DirectionalLight(direction=[0, 1, 0], intensity=0.8))  # Luz desde abajo hacia arriba
rt.lights.append(DirectionalLight(direction=[0.5, 1, -1], intensity=0.8, color=[1, 1, 1]))  # Otra luz desde un ángulo
rt.lights.append(AmbientLight(intensity=0.1))  # Luz ambiental débil

# Creación de 6 esferas en 2 filas (3 arriba, 3 abajo)
#rt.scene.append(Sphere(position=[-1.5, 1, -3], radius=0.5, material=grass))      # Esfera 1 (arriba izquierda)
#rt.scene.append(Sphere(position=[0, 1, -3], radius=0.5, material=grass))         # Esfera 2 (arriba centro)
rt.scene.append(Sphere(position=[1.5, 1, -3], radius=0.5, material=blueMirror))       # Esfera 3 (arriba derecha)
rt.scene.append(Sphere(position=[0, 0, -3], radius=1, material=mirror))  # Esfera grande en el centro
#rt.scene.append(Sphere(position=[-1.5, -1, -3], radius=0.5, material=grass))     # Esfera 4 (abajo izquierda)
#rt.scene.append(Sphere(position=[0, -1, -3], radius=0.5, material=grass))        # Esfera 5 (abajo centro)
#rt.scene.append(Sphere(position=[1.5, -1, -3], radius=0.5, material=grass))      # Esfera 6 (abajo derecha)


# Renderizado de la escena
rt.glRender()

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
