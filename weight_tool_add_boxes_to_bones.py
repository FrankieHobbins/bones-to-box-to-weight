import bpy

print ("---")
newObjectList = []

armature = bpy.context.selected_objects[0].data
#armature.pose_position = 'REST' dont need this if we parent box to bone

#check mesh data for 

for pose_bone in bpy.context.selected_pose_bones:
    #check to see if bone is deform bone
    for bone in armature.bones:
        if pose_bone.name == bone.name:
            if bone.use_deform:
                print (bone.name + "  is getting processed")

                obj = pose_bone.id_data
                matrix_final = obj.matrix_world * pose_bone.matrix            
                pose_bone_size = (pose_bone.head - pose_bone.tail).length
                
                #add cube to bone with vert weight named after bone and set to 1
                bpy.ops.mesh.primitive_cube_add()
                cube = bpy.context.selected_objects[0]    
                cube.name = "WEIGHT_PROXY_" + pose_bone.name
                cube.draw_type = 'WIRE'
                
                for mesh in bpy.data.meshes:
                    if mesh.name == "WEIGHT_PROXY_" + pose_bone.name:
                        cube.data = mesh

                    else:
                        cube.data.name = cube.name
                        
                cube.data.use_fake_user = True
                cube.matrix_world = matrix_final
                cube.scale = cube.scale * pose_bone_size * 0.3
                bpy.ops.transform.translate(value= (0,pose_bone_size*0.5,0), constraint_axis=(False, True, False), constraint_orientation='LOCAL')
                vg = cube.vertex_groups.new(pose_bone.name)
                vg.add(range(0,len(cube.data.vertices)), 1, "ADD")