import bpy
print ("--")

for obj in bpy.data.objects:
    if "WEIGHT_PROXY" in obj.name:
        mode = obj.draw_type

if mode == 'WIRE':
    mode = 'SOLID'

elif mode != 'WIRE':
    mode = 'WIRE'

for obj in bpy.data.objects:
    if "WEIGHT_PROXY" in obj.name:
        obj.draw_type = mode

bpy.context.scene.update()