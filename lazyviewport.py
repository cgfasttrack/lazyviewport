"""Lazy Viewport 1.3

1.3 Updates
- Fixed error on previous versions of blender

1.2 Updates:
- Compatibility with Blender 4.0

1.1 Updates:
Now supporting the modes: 
- Pose Edit Mode
- Armature Edit Mode
- Lattice Edit Mode
- UV Edit Mode
- Metaball Mode
- Pose Mode
"""
import bpy

bl_info = {
    "name": "Lazy Viewport 1.3",
    "blender": (2, 80, 0),
    "category": "Object",
}

addon_keymaps = []

class LazyViewPortMove(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_move"
    bl_label = "Lazy Viewport Move"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_active_tool('builtin.move')
        return {'PASS_THROUGH'}

class LazyViewPortRotate(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_rotate"
    bl_label = "Lazy Viewport Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_active_tool('builtin.rotate')
        return {'PASS_THROUGH'}


class LazyViewPortScale(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_scale"
    bl_label = "Lazy Viewport Scale"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_active_tool('builtin.scale')
        return {'PASS_THROUGH'}


class LazyViewPortSelect(bpy.types.Operator):
    bl_idname = "object.lazy_viewport_select"
    bl_label = "Lazy Viewport Select"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        set_active_tool('builtin.select_box')
        return {'PASS_THROUGH'}


def set_active_tool(tool_name):

    for area in bpy.context.screen.areas:
        types = ['VIEW_3D', 'IMAGE_EDITOR']
        for t in types:
            if area.type == t:
                try:
                    # before 4.0
                    override = bpy.context.copy()
                    override["space_data"] = area.spaces[0]
                    override["area"] = area
                    bpy.ops.wm.tool_set_by_id(override, name=tool_name)
                except:
                    pass

                try:
                    # 4.0 update
                    override = bpy.context.copy()
                    override["space_data"] = area.spaces[0]
                    override["area"] = area
                    override["region"] = area.regions[0]
                    
                    with bpy.context.temp_override(**override):
                        bpy.ops.wm.tool_set_by_id(name=tool_name)
                except:
                    pass


def register():
    bpy.utils.register_class(LazyViewPortMove)
    bpy.utils.register_class(LazyViewPortRotate)
    bpy.utils.register_class(LazyViewPortScale)
    bpy.utils.register_class(LazyViewPortSelect)

    # handle the keymap
    types = ['Object Mode', 'Mesh', 'Curve', 'Lattice', 'Armature', "Metaball", "UV Editor", "Pose"]
    for t in types:
        wm = bpy.context.window_manager
        km = wm.keyconfigs.addon.keymaps.new(name=t, space_type='EMPTY')
        km.keymap_items.new(LazyViewPortMove.bl_idname, 'G', 'PRESS', ctrl=False, shift=False)
        km.keymap_items.new(LazyViewPortRotate.bl_idname, 'R', 'PRESS', ctrl=False, shift=False)
        km.keymap_items.new(LazyViewPortScale.bl_idname, 'S', 'PRESS', ctrl=False, shift=False)
        km.keymap_items.new(LazyViewPortSelect.bl_idname, 'W', 'PRESS', ctrl=False, shift=False)

        addon_keymaps.append(km)

def unregister():
    bpy.utils.unregister_class(LazyViewPortMove)
    bpy.utils.unregister_class(LazyViewPortRotate)
    bpy.utils.unregister_class(LazyViewPortScale)
    bpy.utils.unregister_class(LazyViewPortSelect)


if __name__ == "__main__":
    register()
