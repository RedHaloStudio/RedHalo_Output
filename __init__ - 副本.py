bl_info = {  
    "name": "Output Template",  
    "author": "Red Halo Studio",  
    "version": (0, 1),  
    "blender": (2, 80, 0),  
    "location": "Output",  
    "description": "Set output file template",  
    "wiki_url": "",  
    "tracker_url": "",  
    "category": "Output"
 }

import bpy
from bpy.types import Menu
from bpy.types import Operator
import os
import time
# import re

def setPath(filepath):
    # print(context.scene.RedHalo_Output_Template)
    tempStr = bpy.context.scene.RedHalo_Output_Template

    # 当前输出的路径
    outputFile = bpy.context.scene.render.filepath
    # 当前文件保存路径
    # filepath= os.path.dirname(bpy.data.filepath)
    
    # 当前文件名（无后缀）
    filename = os.path.splitext(bpy.path.basename(bpy.data.filepath))[0]

    # 当前相机名
    try:
        curCamera = bpy.context.scene.camera.name
    except:
        curCamera = ""
    # 当时时间
    curMonth = time.strftime("%m", time.localtime())
    curDay = time.strftime("%d", time.localtime())

    # 模板最终名称
    outTemplate = tempStr.replace("<P>", filename).replace("<C>", curCamera).replace("<M>", curMonth).replace("<D>", curDay)

    outTemplate = os.path.join (filepath , outTemplate)

    return outTemplate

class REDHALO_OT_output_template(Operator):
    bl_idname = "redhalotools.output_template"
    bl_label = "Output Template"
    bl_description = "Output"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath= os.path.dirname(bpy.data.filepath)
        outTemplate = setPath(filepath)
        if filepath != "":
            # bpy.context.scene.render.filepath = os.path.join (filepath , outTemplate)
            bpy.context.scene.render.filepath = outTemplate
        
        return {'FINISHED'}

class REDHALO_OT_Node_fileoutput_template(Operator):
    bl_idname = "redhalotools.fileoutput_template"
    bl_label = "Output Template"
    bl_description = "Output"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # sc = bpy.context.scene
        # sc = sc.data.scenes[sc.name]
        # n = sc.node_tree
        # active=bpy.context.active_object
        active = bpy.context.selected_nodes
        
        if active is not None:
            active_type=active.type
        else:
            active_type=""
        return active_type=='OUTPUT_FILE'
    
    def execute(self, context):
        active = bpy.context.selected_nodes
        print(active)


def draw_menu_output(self, context):
    layout = self.layout
    row = layout.row(align=True)
    # row = layout.column(align=True)
    row.prop(context.scene, "RedHalo_Output_Template")
    row.operator('redhalotools.output_template', icon='WORKSPACE', text = "")

def draw_menu_node_output(self, context):
    layout = self.layout
    row = layout.row(align=True)
    # row = layout.column(align=True)
    row.prop(context.scene, "RedHalo_Output_Template")
    row.operator('redhalotools.fileoutput_template', icon='WORKSPACE', text = "")


def register():
    bpy.utils.register_class(REDHALO_OT_output_template)
    bpy.utils.register_class(REDHALO_OT_Node_fileoutput_template)
    bpy.types.RENDER_PT_output.prepend(draw_menu_output)
    bpy.types.NODE_PT_active_node_properties.prepend(draw_menu_node_output)

    bpy.types.Scene.RedHalo_Output_Template = bpy.props.StringProperty(
        name = "Output Template",
        description = "<P>文件名  <C>相机  <M>月  <D>天",
        default = "tga/<M><D>/<P>_<M><D>"
    )

def unregister():
    # bpy.utils.unregister_class(RedHaloProps)
    bpy.utils.unregister_class(REDHALO_OT_Node_fileoutput_template)
    bpy.utils.unregister_class(REDHALO_OT_output_template)
    bpy.types.NODE_PT_active_node_properties.remove(draw_menu_node_output)
    bpy.types.RENDER_PT_output.remove(draw_menu_output)

    del(bpy.types.Scene.RedHalo_Output_Template)

if __name__ == "__main__":
    register()