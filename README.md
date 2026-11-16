# Abandonados pero no Olvidados · NASA Space Apps Challenge 2026

Visualización interactiva 3D del catálogo oficial **NSSDCA** de la NASA, inspirada en interfaces astronómicas cinematográficas, con exploración del Sistema Solar animado y vistas 3D de superficie para **La Luna** y **Marte**.

## Archivos incluidos en este repositorio
- **`index.html`**: Aplicación web 3D completa (lista para GitHub Pages). Incluye pantalla de inicio, Sistema Solar animado en tiempo real, seguimiento de cámara hacia planetas y sondas, vistas 3D detalladas de la superficie de La Luna y Marte con las 13 misiones de la NASA, modo Malla / Rayos X, línea de tiempo histórica (1960–2026) y botón para cargar modelos `.glb` desde Blender.
- **`escena_la_luna.glb`**, **`escena_marte.glb`**, **`escena_sistema_solar.glb`**: Archivos 3D listos para abrir directamente en Blender (`Archivo > Importar > glTF 2.0`) con terrenos y posiciones exactas.
- **`blender_sistema_solar_animado.py`**, **`blender_escena_luna.py`**, **`blender_escena_marte.py`**: Scripts de Blender con iluminación solar espacial, shaders procedurales de alta definición y gestión de color `AgX`.

## Publicación en GitHub Pages
1. Sube todos los archivos sueltos (descomprimidos) a tu repositorio público en GitHub.
2. Ve a **Settings > Pages**, selecciona la rama **`main`** y carpeta **`/ (root)`**, y guarda.
3. Abre el enlace generado por GitHub Pages para presentar tu proyecto.

## AI / Super Intelligence (SI) Transparency Disclosure
In compliance with the NASA Space Apps Challenge guidelines, we disclose the use of Super Intelligence (SI) tools during the development of this project:

* **Tools Used:** Google Gemini (Versión Hydrogen 4)
* **Scope of Generation:** 
  * **`index.html`:** Assisted in generating the interactive 3D web interface, timeline controls (1960–2026), and `.glb` model loader.
  * **`blender_sistema_solar_animado.py`, `blender_escena_luna.py`, `blender_escena_marte.py`:** Generated the Python scripts for Blender procedural shaders, terrain modifiers, orbital animations, and `AgX` lighting setups.
  * **`README.md` & `.glb` scenes:** Assisted in structuring the documentation and exporting the base 3D scenes (`escena_la_luna.glb`, `escena_marte.glb`, `escena_sistema_solar.glb`).
* **Human Verification & Data:** All historical mission concepts, NASA NSSDCA catalog selections, orbital/surface anchor placements, and final code audits were designed and verified by the team.
