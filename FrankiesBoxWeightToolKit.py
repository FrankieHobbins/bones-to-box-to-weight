import bpy
import bmesh
import random
from mathutils import Vector, Color

bl_info = {
    "name": "Frankies Box Weight Toolkit",
    "author": "Frankie",
    "version": (0,1),
    "blender": (2, 7, 9),
    "location": "View3D > Tool Panel",
    "description": "Lets you set vertex weights with a boxes",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3d View"}

def addBoxesToBones():
    if bpy.context.selected_objects:
        if bpy.context.selected_objects[0].type == 'ARMATURE':
            armatureObj = bpy.context.selected_objects[0]
            armature = bpy.context.selected_objects[0].data

    else:
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE':
                armatureObj = obj
                armature = obj.data

    #add boxes to pose bones only
    for pose_bone in armatureObj.pose.bones:
        if armature.bones[pose_bone.name].use_deform:
            obj = pose_bone.id_data
            pose_bone_size = (pose_bone.head - pose_bone.tail).length
        
            #add cube to bone with vert weight named after bone and set to 1
            bpy.ops.mesh.primitive_cube_add()
            cube = bpy.context.selected_objects[0]
            cube.name = "WEIGHT_PROXY_" + pose_bone.name
            cube.draw_type = 'WIRE'

            #check to see if mesh data allready exists
            preexistingmesh = False 
            for mesh in bpy.data.meshes:
                if mesh.name == "WEIGHT_PROXY_" + pose_bone.name:
                    preexistingmesh = True
                    cube.data = mesh
            if preexistingmesh == False:
                cube.data.name = cube.name

            #setup cube weight proxy
            cube.data.use_fake_user = True #fake user so mesh data persists after WEIGHT_PROXY_ objects have been deleted
            cube.scale = cube.scale * pose_bone_size * 0.3
            cube.parent = armatureObj
            cube.parent_type = 'BONE'
            cube.parent_bone = pose_bone.name
            cube.location = (0,-pose_bone_size*0.5,0)
            
            #add vertex group
            vg = cube.vertex_groups.new(pose_bone.name)
            vg.add(range(0,len(cube.data.vertices)), 1, "ADD")
            
            #lock transforms so that the object cant be changed in a way that isn't saved in the mesh data
            bpy.context.object.lock_location[0] = True
            bpy.context.object.lock_location[1] = True
            bpy.context.object.lock_location[2] = True
            
            bpy.context.object.lock_rotation[0] = True
            bpy.context.object.lock_rotation[1] = True
            bpy.context.object.lock_rotation[2] = True
            
            bpy.context.object.lock_scale[0] = True
            bpy.context.object.lock_scale[1] = True
            bpy.context.object.lock_scale[2] = True
    bpy.context.scene.update()

def removeBoxes():
    for obj in bpy.data.objects:
        if "WEIGHT_PROXY" in obj.name:
            bpy.data.objects.remove(bpy.data.objects[obj.name])
    bpy.context.scene.update()

def changeBoxRenderMode():
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

def getWeightFromBoxes(selObj):
    if selObj.hide == False:
        #sloppy way to add armature to object if not allready there
        hasArmature = False
        for mod in selObj.modifiers:
            if mod.type == 'ARMATURE':
                hasArmature = True
                armature = mod.object
                
        if hasArmature == False:
            bpy.ops.object.modifier_add(type='ARMATURE')
            for obj in bpy.data.objects:
                if obj.type == 'ARMATURE':
                    selObj.modifiers['Armature'].object = obj
                    armature = obj
                    break

        armature.data.pose_position = 'REST'

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

        armature.data.pose_position = 'POSE'

def transferWeights():
    thereHasToBeABetterWay = False

    if bpy.context.selected_objects:
        if bpy.context.selected_objects[0].modifiers:
            for mod in bpy.context.selected_objects[0].modifiers:
                if mod.type == 'ARMATURE':
                    getWeightFromBoxes(bpy.context.selected_objects[0])
                    thereHasToBeABetterWay = True

    if thereHasToBeABetterWay == False:
        for obj in bpy.context.scene.objects:
            if obj.modifiers:
                for mod in obj.modifiers:
                    if mod.type == 'ARMATURE':
                        print(obj)
                        getWeightFromBoxes(obj)
    bpy.context.scene.update()

def smoothWeights():
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

class FBWTK(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Frankies Box Weight Toolkit"
    bl_idname = "OBJECT_PT_boxweightoolkit"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "F BW TK"

    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_ARMATURE', 'POSE'}

    bpy.types.Scene.fvctk_selection = bpy.props.BoolProperty(name="Selected verts only", default=False)
 

    def draw(self, context):
        layout = self.layout

        obj = context.object
        scene = context.scene

        row = layout.row()
        row.operator("vertex_weight.fbwtk_add_boxes_to_bones", text="Add Boxes",icon="OBJECT_DATAMODE")
        row = layout.row()
        row.operator("vertex_weight.fbwtk_remove_boxes_from_bones", text="Remove Boxes",icon="X")
        row = layout.row()
        row.operator("vertex_weight.fbwtk_change_box_render_mode", text="Change Render Mode",icon="MOD_WIREFRAME")
        row = layout.row()
        row.operator("vertex_weight.fbwtk_get_weight_from_boxes", text="Transfer Weights",icon="WPAINT_HLT")
        row = layout.row()
        row.operator("vertex_weight.fbwtk_smooth_weights", text="Smooth Weights",icon="SMOOTHCURVE")

class AddBoxesToBones(bpy.types.Operator):
    bl_idname = "vertex_weight.fbwtk_add_boxes_to_bones"
    bl_label = "Assign"
    bl_description = "Add boxes to bones"

    def execute(self, context):
        addBoxesToBones()
        return{'FINISHED'}

class RemoveBoxesFromBones(bpy.types.Operator):
    bl_idname = "vertex_weight.fbwtk_remove_boxes_from_bones"
    bl_label = "Assign"
    bl_description = "remove boxes from bones"

    def execute(self, context):
        removeBoxes()
        return{'FINISHED'}

class ChangeBoxRenderMode(bpy.types.Operator):
    bl_idname = "vertex_weight.fbwtk_change_box_render_mode"
    bl_label = "Assign"
    bl_description = "change render mode of boxes"

    def execute(self, context):
        changeBoxRenderMode()
        return{'FINISHED'}

class GetWeightFromBoxes(bpy.types.Operator):
    bl_idname = "vertex_weight.fbwtk_get_weight_from_boxes"
    bl_label = "Assign"
    bl_description = "get weight from boxes"

    def execute(self, context):
        transferWeights()
        return{'FINISHED'}

class SmoothWeights(bpy.types.Operator):
    bl_idname = "vertex_weight.fbwtk_smooth_weights"
    bl_label = "Assign"
    bl_description = "smooth weights"

    def execute(self, context):
        smoothWeights()
        return{'FINISHED'}

def register():
    bpy.utils.register_class(FBWTK)
    bpy.utils.register_class(AddBoxesToBones)
    bpy.utils.register_class(RemoveBoxesFromBones)
    bpy.utils.register_class(ChangeBoxRenderMode)
    bpy.utils.register_class(GetWeightFromBoxes)
    bpy.utils.register_class(SmoothWeights)

def unregister():
    bpy.utils.unregister_class(FBWTK)
    bpy.utils.unregister_class(AddBoxesToBones)
    bpy.utils.unregister_class(RemoveBoxesFromBones)
    bpy.utils.unregister_class(ChangeBoxRenderMode)
    bpy.utils.unregister_class(GetWeightFromBoxes)
    bpy.utils.unregister_class(SmoothWeights)
if __name__ == "__main__":
    register()