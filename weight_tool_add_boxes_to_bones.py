import bpy

print ("---")

newObjectList = []

armatureObj = bpy.context.selected_objects[0]
armature = bpy.context.selected_objects[0].data

#armature.pose_position = 'REST' dont need this if we parent box to bone

for pose_bone in bpy.context.selected_pose_bones:
    #check to see if bone is deform bone
    for bone in armature.bones:
        if pose_bone.name == bone.name:
            if bone.use_deform:
                obj = pose_bone.id_data
                pose_bone_size = (pose_bone.head - pose_bone.tail).length
            
                #add cube to bone with vert weight named after bone and set to 1
                bpy.ops.mesh.primitive_cube_add()
                cube = bpy.context.selected_objects[0]    
                cube.name = "WEIGHT_PROXY_" + pose_bone.name
                cube.draw_type = 'WIRE'

                #check to see if mesh data allready exists                 
                for mesh in bpy.data.meshes:
                    if mesh.name == "WEIGHT_PROXY_" + pose_bone.name:
                        cube.data = mesh
                    else:
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