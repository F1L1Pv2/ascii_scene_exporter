bl_info = {
    "name": "AS Exporter",
    "author": "F1L1P (Filip Młodzik)",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "File > Export > Ascii Scene (.json)",
    "description": "Export Ascii Scene",
    "category": "Import-Export",
}

import bpy
import json
import os
from bpy_extras.io_utils import ExportHelper

class ExportAS(bpy.types.Operator, ExportHelper):
    bl_idname = "export.as"
    bl_label = "Export AS"

    filename_ext = ".json"

    def execute(self, context):
        scene = context.scene
        output = []

        for obj in scene.objects:
            if obj.type == 'MESH':
                model_matrix = {
                    "position": list(obj.location),
                    "rotation": list(obj.rotation_euler),
                    "scale": list(obj.scale)
                }

                tags = []
                if "tags" in obj:
                    tags = obj["tags"].split(',')

                texture_path = None
                if obj.data.materials:
                    for slot in obj.material_slots:
                        for node in slot.material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE':
                                texture_path = "/sprites/" + node.image.filepath.split('/')[-1]
                                break
                        if texture_path is not None:
                            break

                output.append({
                    obj.name: {
                        "model_path": "/models/" + obj.name + ".obj",
                        "texture_path": texture_path,
                        "model_matrix": model_matrix,
                        "tags": tags
                    }
                })

        with open(self.filepath, 'w') as f:
            f.write(json.dumps(output, indent=4))

        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportAS.bl_idname, text="Ascii Scene (.json)")

def register():
    bpy.utils.register_class(ExportAS)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.unregister_class(ExportAS)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()