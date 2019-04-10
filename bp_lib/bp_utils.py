import bpy
from bpy_extras import view3d_utils
import mathutils
from mathutils import Vector
import math, random

def get_object_icon(obj):
    ''' 
    This returns the correct icon for the object type

    ARGS
    obj (bpy.types.Object) - Object to get the icon for

    '''
    if obj.type == 'MESH':
        return 'OUTLINER_OB_MESH'
    if obj.type == 'CURVE':
        return 'OUTLINER_OB_CURVE'
    if obj.type == 'FONT':
        return 'OUTLINER_OB_FONT'
    if obj.type == 'EMPTY':
        return 'OUTLINER_OB_EMPTY'
    if obj.type == 'LATTICE':
        return 'OUTLINER_OB_LATTICE'
    if obj.type == 'META':
        return 'OUTLINER_OB_META'                                            
    if obj.type == 'LIGHT':
        return 'OUTLINER_OB_LIGHT'    
    if obj.type == 'CAMERA':
        return 'OUTLINER_OB_CAMERA'    
    if obj.type == 'SURFACE':
        return 'OUTLINER_OB_SURFACE'    
    if obj.type == 'ARMATURE':
        return 'OUTLINER_OB_ARMATURE'    
    if obj.type == 'SPEAKER':
        return 'OUTLINER_OB_SPEAKER'    
    if obj.type == 'FORCE_FIELD':
        return 'OUTLINER_OB_FORCE_FIELD'    
    if obj.type == 'GPENCIL':
        return 'OUTLINER_OB_GREASEPENCIL'    
    if obj.type == 'LIGHT_PROBE':
        return 'OUTLINER_OB_LIGHTPROBE'  

def delete_obj_list(obj_list):
    ''' 
    This function deletes every object in the list
    '''
    bpy.ops.object.select_all(action='DESELECT')
    for obj in obj_list:
        if obj.animation_data:
            for driver in obj.animation_data.drivers:
                # THESE DRIVERS MUST BE REMOVED TO DELETE OBJECTS
                if driver.data_path in {'hide','hide_select'}: 
                    obj.driver_remove(driver.data_path) 
        
        obj.parent = None
        obj.hide_select = False
        obj.hide_viewport = False
        obj.select = True
        
        if obj.name in bpy.context.scene.objects:
            bpy.context.scene.objects.unlink(obj)

    for obj in obj_list:
        bpy.data.objects.remove(obj,do_unlink=True)

def delete_object_and_children(obj_bp):
    '''
    Deletes a object and all it's children

    ARGS
    obj_bp (bpy.types.Object) - Parent Object to Delete
    '''
    obj_list = []
    obj_list.append(obj_bp)
    for child in obj_bp.children:
        if len(child.children) > 0:
            delete_object_and_children(child)
        else:
            obj_list.append(child)
    delete_obj_list(obj_list)

def floor_raycast(context, mx, my):
    '''
    This casts a ray into the 3D view and returns information based on what is under the mouse

    ARGS
    context (bpy.context) = current blender context
    mx (float) = 2D mouse x location
    my (float) = 2D mouse y location

    RETURNS tuple
    has_hit (boolean) - determines if an object is under the mouse
    snapped_location (tuple) - x,y,z location of location under mouse
    snapped_normal (tuple) - normal direction
    snapped_rotation (tuple) - rotation
    face_index (int) - face index under mouse
    object (bpy.types.Object) - Blender Object under mouse
    martix (float multi-dimensional array of 4 * 4 items in [-inf, inf]) - matrix of placement under mouse
    '''
    r = context.region
    rv3d = context.region_data
    coord = mx, my

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(r, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(r, rv3d, coord)
    # ray_target = ray_origin + (view_vector * 1000000000)
    ray_target = ray_origin + view_vector

    snapped_location = mathutils.geometry.intersect_line_plane(ray_origin, ray_target, (0, 0, 0), (0, 0, 1),
                                                               False)
    if snapped_location != None:
        has_hit = True
        snapped_normal = Vector((0, 0, 1))
        face_index = None
        object = None
        matrix = None
        snapped_rotation = snapped_normal.to_track_quat('Z', 'Y').to_euler()
        offset_rotation_amount = 0
        randomize_rotation_amount = 0
        randomize_rotation = False
        if randomize_rotation:
            randoffset = offset_rotation_amount + math.pi + (
                    random.random() - 0.5) * randomize_rotation_amount
        else:
            randoffset = offset_rotation_amount + math.pi
        snapped_rotation.rotate_axis('Z', randoffset)

    return has_hit, snapped_location, snapped_normal, snapped_rotation, face_index, object, matrix