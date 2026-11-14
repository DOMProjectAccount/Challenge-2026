# Proyecto 3D NASA Space Apps Challenge 2026

Este paquete contiene los archivos listos para abrir en tu navegador y para editar directamente en Blender:

## 1. Archivos incluidos
- **`escena_nasa_base.glb`**: Escena 3D lista para importar en Blender con los terrenos con crateres de La Luna y Marte, materiales PBR y los puntos ubicados de todas las misiones (Apolo Eagle, LRV, ALSEP, Sojourner, Spirit/Opportunity, Viking 1 y 2, Phoenix/InSight, Ingenuity, Dawn, NEAR Shoemaker, Pioneer 10/11 y Kepler).
- **`escena_blender_nasa.py`**: Script automatico para Blender que crea colecciones organizadas, terrenos subdivididos con modificador Displace, luces espaciales y camara principal.
- **`index.html`**: Aplicacion web interactiva en 3D (WebGL / Three.js) con vista dividida Luna/Marte, tarjetas de telemetria del NSSDCA, buscador, linea de tiempo (1960-2026), modo malla (Rayos X) y boton para cargar tus archivos `.glb` exportados desde Blender.

## 2. Como abrir y editar en Blender en 3 pasos
1. Abre **Blender**.
2. Ve al menu superior **Archivo > Importar > glTF 2.0 (.glb/.gltf)** y selecciona **`escena_nasa_base.glb`**.
3. En el panel derecho (*Outliner*) veras cada terreno y nave separados por nombre para que puedas esculpir, cambiar materiales o sustituir cada bloque por los modelos oficiales de `science.nasa.gov/3d-resources`.

*(Opcional)* Si prefieres generar la escena procedural con modificadores editables en Blender: ve a la pestana **Scripting**, abre **`escena_blender_nasa.py`** y presiona el boton **Play (Ejecutar script)**.

## 3. Como ejecutar la pagina web 3D
- Haz doble clic sobre **`index.html`** para abrirlo en Chrome, Edge o Firefox (si usas VS Code, puedes abrirlo con *Live Server*).
