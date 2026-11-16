"""
Blender 3D Scene Generation Script - NASA Space Apps Challenge 2026.
Project: Forgotten Giants (Official NASA NSSDCA Spacecraft Catalog).

AI / Super Intelligence (SI) Disclosure:
This script was generated with assistance from Google Gemini (Version Hydrogen 4) to 
build procedural planetary geometry, lighting, and mission anchors. All code and spatial 
parameters were reviewed and validated by Team Forgotten Giants.
"""

__author__ = "Team Forgotten Giants"
__credits__ = ["Team Forgotten Giants", "Google Gemini - Version Hydrogen 4 (Code Generation Assistance)"]
__ai_disclosure__ = {
    "si_generated": True,
    "tool": "Google Gemini",
    "version": "Hydrogen 4",
    "project": "Forgotten Giants",
    "challenge": "NASA Space Apps Challenge 2026",
    "human_verified": True
}



import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in engines else 'BLENDER_EEVEE'

try:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - High Contrast'
except Exception:
    scene.view_settings.view_transform = 'Filmic'

col_terreno = bpy.data.collections.new("01_SUPERFICIE_LUNAR")
col_misiones = bpy.data.collections.new("02_MODULOS_Y_ROVERS_LUNA")
scene.collection.children.link(col_terreno)
scene.collection.children.link(col_misiones)

# Terreno lunar de alta resolucion (128x128)
bpy.ops.mesh.primitive_grid_add(x_subdivisions=128, y_subdivisions=128, size=12.0, location=(0, 0, 0))
terreno = bpy.context.active_object
terreno.name = "Superficie_La_Luna"
for c in terreno.users_collection:
    c.objects.unlink(terreno)
col_terreno.objects.link(terreno)

# Modificador 1: Crateres grandes (Voronoi)
tex_crater = bpy.data.textures.new("Crateres_Grandes_Luna", type='VORONOI')
tex_crater.noise_scale = 2.4
tex_crater.distance_metric = 'DISTANCE_SQUARED'
mod1 = terreno.modifiers.new("Crateres_Principales", type='DISPLACE')
mod1.texture = tex_crater
mod1.strength = 0.65

# Modificador 2: Micro-crateres y rugosidad
tex_micro = bpy.data.textures.new("Micro_Crateres_Luna", type='CLOUDS')
tex_micro.noise_scale = 0.65
mod2 = terreno.modifiers.new("Detalle_Regolito", type='DISPLACE')
mod2.texture = tex_micro
mod2.strength = 0.14

bpy.ops.object.shade_smooth()

# Shader fotorrealista de regolito lunar con Bump procedural
mat = bpy.data.materials.new("Mat_Regolito_Lunar_HD")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.94
if "Specular IOR Level" in bsdf.inputs:
    bsdf.inputs["Specular IOR Level"].default_value = 0.18

noise = nt.nodes.new("ShaderNodeTexNoise")
noise.inputs["Scale"].default_value = 18.0
noise.inputs["Detail"].default_value = 10.0
noise.inputs["Roughness"].default_value = 0.75

ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.25
ramp.color_ramp.elements[0].color = (0.14, 0.15, 0.17, 1.0)
ramp.color_ramp.elements[1].position = 0.78
ramp.color_ramp.elements[1].color = (0.42, 0.44, 0.47, 1.0)

bump = nt.nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.45
bump.inputs["Distance"].default_value = 0.05

nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
terreno.data.materials.append(mat)

# Anclas (Empties) exactas para colocar los modelos .GLB de la NASA
anclas_luna = [
    ("Modulo_Lunar_Apolo_Eagle", (-1.8, -1.2, 0.32)),
    ("Vehiculo_Lunar_LRV", (1.6, 0.9, 0.25)),
    ("Paquetes_Cientificos_ALSEP", (-0.5, 2.1, 0.22)),
    ("Sondas_Roboticas_Reconocimiento", (2.3, -1.9, 0.28)),
]
for nombre, pos in anclas_luna:
    emp = bpy.data.objects.new(nombre, None)
    emp.empty_display_type = 'ARROWS'
    emp.empty_display_size = 0.65
    emp.location = pos
    emp.show_name = True
    col_misiones.objects.link(emp)

# Iluminacion espacial dura (Sol sin atmosfera = sombras nitidas)
sol_data = bpy.data.lights.new("Sol_Lunar", type='SUN')
sol_data.energy = 5.5
sol_data.angle = math.radians(0.53)
sol_obj = bpy.data.objects.new("Sol_Lunar", sol_data)
sol_obj.rotation_euler = (math.radians(68), math.radians(10), math.radians(-42))
scene.collection.objects.link(sol_obj)

world = bpy.data.worlds.new("Cielo_Negro_Luna")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.002, 0.003, 0.007, 1.0)

cam_data = bpy.data.cameras.new("Camara_Luna")
cam_obj = bpy.data.objects.new("Camara_Luna", cam_data)
cam_obj.location = (0.0, -7.8, 3.6)
cam_obj.rotation_euler = (math.radians(66), 0, 0)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

print("Escena HD de La Luna lista. Importa tus modelos .GLB y copia la ubicacion de las anclas.")
