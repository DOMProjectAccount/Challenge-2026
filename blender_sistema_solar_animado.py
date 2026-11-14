import bpy
import math

# Reiniciar escena limpia
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# Motor de render compatible con Blender 3.6 / 4.x
engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in engines else 'BLENDER_EEVEE'

# Gestion de color cinematografica
try:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    scene.view_settings.view_transform = 'Filmic'

scene.frame_start = 1
scene.frame_end = 240

# Colecciones
col_sol = bpy.data.collections.new("01_SOL_Y_ORBITAS")
col_planetas = bpy.data.collections.new("02_TIERRA_LUNA_MARTE")
col_sondas = bpy.data.collections.new("03_SONDAS_ESPACIO_PROFUNDO")
scene.collection.children.link(col_sol)
scene.collection.children.link(col_planetas)
scene.collection.children.link(col_sondas)

def mover_a_coleccion(obj, col):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)

def set_linear_interpolation(obj):
    if obj.animation_data and obj.animation_data.action:
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'LINEAR'

# 1. SOL EMISIVO + LUZ PUNTUAL CENTRAL
bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=1.35, location=(0, 0, 0))
sol = bpy.context.active_object
sol.name = "Sol"
bpy.ops.object.shade_smooth()
mover_a_coleccion(sol, col_sol)

mat_sol = bpy.data.materials.new("Mat_Sol_Emision")
mat_sol.use_nodes = True
nodes = mat_sol.node_tree.nodes
bsdf_sol = nodes.get("Principled BSDF")
bsdf_sol.inputs["Base Color"].default_value = (1.0, 0.65, 0.1, 1.0)
if "Emission Color" in bsdf_sol.inputs:
    bsdf_sol.inputs["Emission Color"].default_value = (1.0, 0.58, 0.08, 1.0)
    bsdf_sol.inputs["Emission Strength"].default_value = 8.5
sol.data.materials.append(mat_sol)

luz_sol_data = bpy.data.lights.new("Luz_Solar_Central", type='POINT')
luz_sol_data.energy = 2500.0
luz_sol_data.color = (1.0, 0.94, 0.85)
luz_sol_data.shadow_soft_size = 0.6
luz_sol = bpy.data.objects.new("Luz_Solar_Central", luz_sol_data)
col_sol.objects.link(luz_sol)

# Helper para crear anillos orbitales visibles
def crear_anillo_orbita(nombre, radio):
    bpy.ops.curve.primitive_bezier_circle_add(radius=radio, location=(0, 0, 0))
    orb = bpy.context.active_object
    orb.name = nombre
    orb.data.bevel_depth = 0.012
    orb.data.resolution_u = 64
    mover_a_coleccion(orb, col_sol)
    mat_o = bpy.data.materials.new(f"Mat_{nombre}")
    mat_o.use_nodes = True
    b = mat_o.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (0.25, 0.45, 0.75, 1.0)
    if "Emission Color" in b.inputs:
        b.inputs["Emission Color"].default_value = (0.2, 0.4, 0.7, 1.0)
        b.inputs["Emission Strength"].default_value = 1.2
    orb.data.materials.append(mat_o)
    return orb

crear_anillo_orbita("Orbita_Tierra", 4.2)
crear_anillo_orbita("Orbita_Marte", 6.8)
crear_anillo_orbita("Orbita_Cinturon_Dawn", 9.2)

# 2. PIVOTE Y PLANETA TIERRA + LUNA
pivote_tierra = bpy.data.objects.new("Pivote_Orbita_Tierra", None)
col_planetas.objects.link(pivote_tierra)

bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.45, location=(4.2, 0, 0))
tierra = bpy.context.active_object
tierra.name = "Planeta_Tierra"
bpy.ops.object.shade_smooth()
mover_a_coleccion(tierra, col_planetas)
tierra.parent = pivote_tierra

mat_tierra = bpy.data.materials.new("Mat_Tierra_Procedural")
mat_tierra.use_nodes = True
nt = mat_tierra.node_tree
noise_t = nt.nodes.new("ShaderNodeTexNoise")
noise_t.inputs["Scale"].default_value = 3.2
ramp_t = nt.nodes.new("ShaderNodeValToRGB")
ramp_t.color_ramp.elements[0].position = 0.46
ramp_t.color_ramp.elements[0].color = (0.04, 0.18, 0.65, 1.0)
ramp_t.color_ramp.elements[1].position = 0.54
ramp_t.color_ramp.elements[1].color = (0.12, 0.45, 0.22, 1.0)
nt.links.new(noise_t.outputs["Fac"], ramp_t.inputs["Fac"])
nt.links.new(ramp_t.outputs["Color"], nt.nodes["Principled BSDF"].inputs["Base Color"])
tierra.data.materials.append(mat_tierra)

# Pivote Lunar alrededor de la Tierra
pivote_luna = bpy.data.objects.new("Pivote_Orbita_Luna", None)
pivote_luna.location = (4.2, 0, 0)
col_planetas.objects.link(pivote_luna)
pivote_luna.parent = pivote_tierra

bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.14, location=(0.85, 0, 0))
luna = bpy.context.active_object
luna.name = "La_Luna"
bpy.ops.object.shade_smooth()
mover_a_coleccion(luna, col_planetas)
luna.parent = pivote_luna

# 3. PIVOTE Y PLANETA MARTE
pivote_marte = bpy.data.objects.new("Pivote_Orbita_Marte", None)
pivote_marte.rotation_euler = (0, 0, math.radians(135))
col_planetas.objects.link(pivote_marte)

bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=0.36, location=(6.8, 0, 0))
marte = bpy.context.active_object
marte.name = "Planeta_Marte"
bpy.ops.object.shade_smooth()
mover_a_coleccion(marte, col_planetas)
marte.parent = pivote_marte

mat_marte = bpy.data.materials.new("Mat_Marte_Procedural")
mat_marte.use_nodes = True
nm = mat_marte.node_tree
noise_m = nm.nodes.new("ShaderNodeTexNoise")
noise_m.inputs["Scale"].default_value = 5.0
ramp_m = nm.nodes.new("ShaderNodeValToRGB")
ramp_m.color_ramp.elements[0].position = 0.35
ramp_m.color_ramp.elements[0].color = (0.35, 0.10, 0.04, 1.0)
ramp_m.color_ramp.elements[1].position = 0.70
ramp_m.color_ramp.elements[1].color = (0.82, 0.32, 0.14, 1.0)
nm.links.new(noise_m.outputs["Fac"], ramp_m.inputs["Fac"])
nm.links.new(ramp_m.outputs["Color"], nm.nodes["Principled BSDF"].inputs["Base Color"])
marte.data.materials.append(mat_marte)

# 4. ANCLAS PARA SONDAS DEL ESPACIO PROFUNDO
sondas = [
    ("Voyager_1", (-8.5, 5.5, 2.2)),
    ("Voyager_2", (8.8, -5.2, -1.8)),
    ("Pioneer_10_y_11", (-9.2, -4.8, 1.1)),
    ("Nave_Dawn_Ceres", (9.2, 0.0, 0.3)),
    ("NEAR_Shoemaker_Eros", (-5.5, 3.8, -0.4)),
    ("Telescopio_Kepler", (4.6, -1.2, 0.2)),
]
for nombre, pos in sondas:
    emp = bpy.data.objects.new(nombre, None)
    emp.empty_display_type = 'ARROWS'
    emp.empty_display_size = 0.5
    emp.location = pos
    emp.show_name = True
    col_sondas.objects.link(emp)

# 5. ANIMACION ORBITAL CONTINUA (240 FRAMES)
pivote_tierra.rotation_euler = (0, 0, 0)
pivote_tierra.keyframe_insert(data_path="rotation_euler", frame=1)
pivote_tierra.rotation_euler = (0, 0, math.radians(360))
pivote_tierra.keyframe_insert(data_path="rotation_euler", frame=241)
set_linear_interpolation(pivote_tierra)

pivote_luna.rotation_euler = (0, 0, 0)
pivote_luna.keyframe_insert(data_path="rotation_euler", frame=1)
pivote_luna.rotation_euler = (0, 0, math.radians(360 * 4))
pivote_luna.keyframe_insert(data_path="rotation_euler", frame=241)
set_linear_interpolation(pivote_luna)

pivote_marte.rotation_euler = (0, 0, math.radians(135))
pivote_marte.keyframe_insert(data_path="rotation_euler", frame=1)
pivote_marte.rotation_euler = (0, 0, math.radians(135 + 180))
pivote_marte.keyframe_insert(data_path="rotation_euler", frame=241)
set_linear_interpolation(pivote_marte)

# Fondo negro espacio profundo + Camara
world = bpy.data.worlds.new("Espacio_Negro")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.006, 0.014, 1.0)

cam_data = bpy.data.cameras.new("Camara_Sistema_Solar")
cam_obj = bpy.data.objects.new("Camara_Sistema_Solar", cam_data)
cam_obj.location = (0.0, -14.5, 8.2)
cam_obj.rotation_euler = (math.radians(60), 0, 0)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

print("Sistema Solar animado creado. Presiona BARRA ESPACIADORA para reproducir.")
