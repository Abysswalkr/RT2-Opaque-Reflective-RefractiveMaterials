# Ray Tracing Esferas con Texturas

Este proyecto es un renderizador simple de esferas utilizando **Ray Tracing** con soporte para **texturas** y diferentes tipos de materiales como opacos, reflectivos y transparentes. Las esferas pueden tener texturas aplicadas y la escena está iluminada con fuentes de luz configurables.

## Características

- **Soporte de texturas**: Aplica imágenes a las esferas utilizando coordenadas UV.
- **Materiales avanzados**: Las esferas pueden ser opacas, reflectivas o transparentes, con parámetros configurables como difusividad, especularidad y índice de refracción (IOR).
- **Reflexión y refracción**: Soporte completo para efectos de reflexión y refracción en materiales reflectivos y transparentes.
- **Entorno dinámico**: Soporte para un **mapa de entorno** que se refleja en las esferas.
- **Iluminación configurable**: Implementa luces direccionales y ambientales para controlar el ambiente de la escena.

## Requisitos Previos

Asegúrate de tener **Python** y **Pygame** instalados para ejecutar este proyecto.

Puedes instalar Pygame ejecutando:

```bash
pip install pygame
```

## Instalación

1. Clona este repositorio y navega al directorio del proyecto:

    ```sh
    git clone https://github.com/tu-usuario/raytracing-esferas-texturas.git
    cd raytracing-esferas-texturas
    ```

2. Asegúrate de tener las texturas correctas en la carpeta **Textures**. Incluye las imágenes de fondo y las que desees usar como texturas para las esferas.

3. Ejecuta el archivo principal del renderizador para iniciar el proyecto:

    ```sh
    python Raytracer.py
    ```

## Uso

El proyecto mostrará seis esferas en pantalla con diferentes texturas aplicadas. Las esferas pueden ser configuradas con diferentes tipos de materiales y efectos de reflexión y refracción.

### Estructura del Proyecto

- **Raytracer.py**: Archivo principal que inicializa el renderizador y define las esferas con sus texturas y materiales.
- **gl.py**: Renderizador de Ray Tracing que maneja la lógica principal del trazado de rayos, incluyendo el manejo de luces, texturas y efectos de reflexión/refracción.
- **figures.py**: Define las figuras geométricas que se renderizan, principalmente las esferas.
- **material.py**: Contiene la lógica para los diferentes tipos de materiales aplicables a las esferas.
- **textures**: Carpeta que contiene las texturas utilizadas en las esferas y el fondo.

### Ejemplo de Configuración de Esferas

En el archivo **Raytracer.py**, puedes configurar una esfera con una textura de la siguiente manera:

```python
# Cargar una textura y aplicarla a una esfera
earth_texture = Material(texture=Texture('Textures/earth.bmp'), spec=128, Ks=0.2)
rt.scene.append(Sphere(position=[1.5, 1, -3], radius=0.5, material=earth_texture))
```

## Materiales y Texturas

El sistema de materiales soporta los siguientes tipos:

- **Difusos**: Un color base que interactúa con la luz de manera uniforme.
- **Reflectivos**: Materiales que generan reflejos en las superficies.
- **Transparentes**: Soporte para refracción de luz a través de las esferas.

### Parámetros de Materiales

- `spec`: Determina el brillo especular.
- `Ks`: Coeficiente de especularidad (entre 0 y 1).
- `ior`: Índice de refracción (solo para materiales transparentes).
- `matType`: Determina si el material es opaco, reflectivo o transparente.

## Captura de Pantalla

![Captura de pantalla 2024-09-25 220412](https://github.com/user-attachments/assets/1cdc1a19-68d5-4d4a-abcb-fbefb841f320)

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar este proyecto, por favor abre un issue o crea un pull request.
