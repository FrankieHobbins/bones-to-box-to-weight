import bpy

for mesh in bpy.data.meshes:
    if "WEIGHT_PROXY_" in mesh.name:
        mesh.use_fake_user = False