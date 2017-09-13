import bpy

for obj in bpy.data.objects:
    if "WEIGHT_PROXY" in obj.name:
        bpy.data.objects.remove(bpy.data.objects[obj.name])
        
bpy.context.scene.update()        