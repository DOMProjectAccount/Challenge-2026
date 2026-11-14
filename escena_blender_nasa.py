import bpy
import math
import random

# Limpiar escena actual
bpy.ops.wm.read_factory_settings(use_empty=True)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'

# Crear colecciones organizadas
col_luna = bpy.data.collections.new("01_LA_LUNA")
col_marte = bpy.data.collections.new("02_MARTE")
col_espacio = bpy.data.collections.new("03_ESPACIO_PROFUNDO")
scene.collection.children.link(col_luna)
scene.collection.children.link(col_marte)
scene.collection.children.link(col_espacio)

def crear_material_planetario(nombre, color_base, rugosidad=0.9):
    mat = bpy.data.materials.new(name=nombre)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color_base
    bsdf.inputs["Roughness"].default_value = rugosidad
    return mat

mat_luna = crear_material_planetario("Regolito_Lunar", (0.28, 0.30, 0.34, 1.0), 0.95)
mat_marte = crear_material_planetario("Suelo_Marciano", (0.62, 0.22, 0.10, 1.0), 0.90)

def crear_terreno(nombre, ubicacion, coleccion, material, escala_ruido=3.5, fuerza=0.55):
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=96, y_subdivisions=96, size=8.5, location=ubicacion)
    terreno = bpy.context.active_object
    terreno.name = nombre
    
    # Mover a su coleccion
    for c in terreno.users_collection:
        c.objects.unlink(terreno)
    coleccion.objects.link(terreno)
    terreno.data.materials.append(material)
    
    # Textura procedural de crateres
    tex = bpy.data.textures.new(name=f"Tex_{nombre}", type='VORONOI')
    tex.noise_scale = escala_ruido
    tex.distance_metric = 'DISTANCE_SQUARED'
    
    mod = terreno.modifiers.new(name="Relieve_Crateres", type='DISPLACE')
    mod.texture = tex
    mod.strength = fuerza
    
    bpy.ops.object.shade_smooth()
    return terreno

crear_terreno("Superficie_Lunar", (-4.8, 0.0, 0.0), col_luna, mat_luna, escala_ruido=2.8, fuerza=0.5)
crear_terreno("Superficie_Marciana", (4.8, 0.0, 0.0), col_marte, mat_marte, escala_ruido=3.4, fuerza=0.65)

# Puntos de anclaje (Empties) listos para reemplazar con los .GLB de la NASA
misiones_luna = [
    ("Modulo_Lunar_Apolo_Eagle", (-5.6, -1.2, 0.4)),
    ("Vehiculo_Lunar_LRV", (-4.1, 0.8, 0.3)),
    ("Paquetes_Cientificos_ALSEP", (-5.2, 1.9, 0.25)),
    ("Sondas_Roboticas_Reconocimiento", (-3.6, -2.0, 0.3)),
]

misiones_marte = [
    ("Rover_Sojourner", (3.6, -1.5, 0.3)),
    ("Spirit_y_Opportunity", (5.2, 0.2, 0.35)),
    ("Modulos_Viking_1_y_2", (4.0, 2.0, 0.3)),
    ("Phoenix_e_InSight", (6.2, 1.5, 0.3)),
    ("Helicoptero_Ingenuity", (5.0, 2.4, 1.3)),
]

misiones_espacio = [
    ("Dawn_Vesta_Ceres", (-4.5, -2.5, 3.5)),
    ("NEAR_Shoemaker_Eros", (-1.5, -2.5, 3.7)),
    ("Pioneer_10_y_11", (1.5, -2.5, 3.7)),
    ("Telescopio_Kepler", (4.5, -2.5, 3.5)),
]

def crear_anclas(lista, coleccion):
    for nombre, pos in lista:
        empty = bpy.data.objects.new(nombre, None)
        empty.empty_display_type = 'ARROWS'
        empty.empty_display_size = 0.55
        empty.location = pos
        empty.show_name = True
        coleccion.objects.link(empty)

crear_anclas(misiones_luna, col_luna)
crear_anclas(misiones_marte, col_marte)
crear_anclas(misiones_espacio, col_espacio)

# Iluminacion espacial
luz_data = bpy.data.lights.new(name="Sol_Espacial", type='SUN')
luz_data.energy = 4.2
luz_obj = bpy.data.objects.new(name="Sol_Espacial", object_data=luz_data)
luz_obj.rotation_euler = (math.radians(55), math.radians(15), math.radians(-35))
scene.collection.objects.link(luz_obj)

# Camara principal
cam_data = bpy.data.cameras.new(name="Camara_Principal")
cam_obj = bpy.data.objects.new(name="Camara_Principal", object_data=cam_data)
cam_obj.location = (0.0, -13.5, 6.8)
cam_obj.rotation_euler = (math.radians(64), 0.0, 0.0)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

# Fondo oscuro espacial
world = bpy.data.worlds.new("Espacio_Profundo")
scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get("Background")
bg.inputs["Color"].default_value = (0.012, 0.018, 0.035, 1.0)

print("Escena NASA Space Apps 2026 generada con exito.")
