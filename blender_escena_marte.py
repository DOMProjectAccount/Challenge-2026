import bpy
import math

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items]
scene.render.engine = 'BLENDER_EEVEE_NEXT' if 'BLENDER_EEVEE_NEXT' in engines else 'BLENDER_EEVEE'

try:
    scene.view_settings.view_transform = 'AgX'
    scene.view_settings.look = 'AgX - Medium High Contrast'
except Exception:
    scene.view_settings.view_transform = 'Filmic'

col_terreno = bpy.data.collections.new("01_SUPERFICIE_MARCIANA")
col_misiones = bpy.data.collections.new("02_ROVERS_Y_MODULOS_MARTE")
scene.collection.children.link(col_terreno)
scene.collection.children.link(col_misiones)

bpy.ops.mesh.primitive_grid_add(x_subdivisions=128, y_subdivisions=128, size=12.0, location=(0, 0, 0))
terreno = bpy.context.active_object
terreno.name = "Superficie_Marte"
for c in terreno.users_collection:
    c.objects.unlink(terreno)
col_terreno.objects.link(terreno)

# Relieve rocoso y crateres marcianos
tex_dunas = bpy.data.textures.new("Dunas_Crateres_Marte", type='VORONOI')
tex_dunas.noise_scale = 3.1
tex_dunas.distance_metric = 'DISTANCE_SQUARED'
mod1 = terreno.modifiers.new("Relieve_Marciano", type='DISPLACE')
mod1.texture = tex_dunas
mod1.strength = 0.72

tex_rocas = bpy.data.textures.new("Rocas_Marte", type='MUSGRAVE')
tex_rocas.noise_scale = 0.85
mod2 = terreno.modifiers.new("Detalle_Rocoso", type='DISPLACE')
mod2.texture = tex_rocas
mod2.strength = 0.18

bpy.ops.object.shade_smooth()

# Shader oxido de hierro marciano
mat = bpy.data.materials.new("Mat_Suelo_Marciano_HD")
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes["Principled BSDF"]
bsdf.inputs["Roughness"].default_value = 0.89

noise = nt.nodes.new("ShaderNodeTexNoise")
noise.inputs["Scale"].default_value = 14.0
noise.inputs["Detail"].default_value = 9.0

ramp = nt.nodes.new("ShaderNodeValToRGB")
ramp.color_ramp.elements[0].position = 0.25
ramp.color_ramp.elements[0].color = (0.26, 0.08, 0.03, 1.0)
ramp.color_ramp.elements[1].position = 0.78
ramp.color_ramp.elements[1].color = (0.76, 0.28, 0.11, 1.0)

bump = nt.nodes.new("ShaderNodeBump")
bump.inputs["Strength"].default_value = 0.5
bump.inputs["Distance"].default_value = 0.06

nt.links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
nt.links.new(noise.outputs["Fac"], bump.inputs["Height"])
nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
terreno.data.materials.append(mat)

# Anclas (Empties) exactas para los Rovers y Modulos en Marte
anclas_marte = [
    ("Rover_Sojourner", (-2.2, -1.4, 0.28)),
    ("Rovers_Spirit_y_Opportunity", (0.8, 0.3, 0.32)),
    ("Modulos_Viking_1_y_2", (-1.5, 2.0, 0.30)),
    ("Modulos_Phoenix_e_InSight", (2.4, 1.6, 0.30)),
    ("Helicoptero_Ingenuity", (0.4, 2.2, 1.35)),
]
for nombre, pos in anclas_marte:
    emp = bpy.data.objects.new(nombre, None)
    emp.empty_display_type = 'ARROWS'
    emp.empty_display_size = 0.65
    emp.location = pos
    emp.show_name = True
    col_misiones.objects.link(emp)

# Luz solar marciana + luz de rebote atmosferico
sol_data = bpy.data.lights.new("Sol_Marciano", type='SUN')
sol_data.energy = 4.6
sol_data.color = (1.0, 0.90, 0.80)
sol_obj = bpy.data.objects.new("Sol_Marciano", sol_data)
sol_obj.rotation_euler = (math.radians(60), math.radians(15), math.radians(-35))
scene.collection.objects.link(sol_obj)

world = bpy.data.worlds.new("Atmosfera_Marciana")
scene.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.045, 0.016, 0.008, 1.0)
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45

cam_data = bpy.data.cameras.new("Camara_Marte")
cam_obj = bpy.data.objects.new("Camara_Marte", cam_data)
cam_obj.location = (0.0, -7.8, 3.6)
cam_obj.rotation_euler = (math.radians(66), 0, 0)
scene.collection.objects.link(cam_obj)
scene.camera = cam_obj

print("Escena HD de Marte lista. Importa tus Rovers .GLB y copia la ubicacion de las anclas.")
