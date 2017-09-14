import bpy
print ("--")

for obj in bpy.data.objects:
    if "WEIGHT_PROXY" in obj.name:
        if obj.draw_type == 'WIRE':        
            obj.draw_type = 'SOLID'
            continue
            
        if obj.draw_type == 'SOLID':
            obj.draw_type = 'WIRE'
            continue

bpy.context.scene.update()