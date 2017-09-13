import bpy

print ("---")

selObj = bpy.context.selected_objects[0]

try:
    bpy.ops.object.modifier_remove(modifier="DELETE_ME_WP")
except:
    print("what")

try:
    bpy.data.objects.remove(bpy.data.objects["DELETE_ME_WP"])
except:
    print("what")

#remove all vertex groups
for group in selObj.vertex_groups:
    selObj.vertex_groups.remove(group)

#join all bone boxes into one object called "DELETE_ME_WP"
for obj in bpy.data.objects:
    obj.select = False
    if "WEIGHT_PROXY_" in obj.name:
        obj.select = True
        bpy.context.scene.objects.active = obj
        
bpy.ops.object.duplicate_move()
bpy.ops.object.join()
bpy.context.selected_objects[0].name = "DELETE_ME_WP"

bpy.ops.object.select_all(action='TOGGLE')

bpy.context.scene.objects.active = selObj
selObj.select = True

#apply data transfer to selOBJ from "DELETE_ME_WP"
bpy.ops.object.modifier_add(type='DATA_TRANSFER')
selObj.modifiers[len(selObj.modifiers)-1].name = "DELETE_ME_WP"

while selObj.modifiers[0].name != "DELETE_ME_WP":
    bpy.ops.object.modifier_move_up(modifier="DELETE_ME_WP")

selObj.modifiers["DELETE_ME_WP"].use_vert_data = True
selObj.modifiers["DELETE_ME_WP"].data_types_verts = {'VGROUP_WEIGHTS'}
selObj.modifiers["DELETE_ME_WP"].vert_mapping = 'POLY_NEAREST'
selObj.modifiers["DELETE_ME_WP"].object = bpy.data.objects["DELETE_ME_WP"]

bpy.ops.object.datalayout_transfer(modifier="DELETE_ME_WP")

#enable use_paint_mask_vertex 
#select all verts bpy.ops.paint.vert_select_all(action='TOGGLE')
#loop all vert groups and do bpy.ops.object.vertex_group_smooth()

bpy.ops.object.modifier_apply(apply_as='DATA', modifier="DELETE_ME_WP")

bpy.ops.object.modifier_remove(modifier="DELETE_ME_WP")
bpy.data.objects.remove(bpy.data.objects["DELETE_ME_WP"])

# armature.pose_position = 'POSE'