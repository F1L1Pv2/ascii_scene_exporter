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
        exported_meshes = set()

        scene_name = self.filepath.split('/')[-1]
        filepath = '/'.join(self.filepath.split('/')[:-1])

        # Create directories if they don't exist
        models_dir = os.path.join(filepath, "models")
        scenes_dir = os.path.join(filepath, "scenes")
        sprites_dir = os.path.join(filepath, "sprites")
        os.makedirs(models_dir, exist_ok=True)
        os.makedirs(scenes_dir, exist_ok=True)
        os.makedirs(sprites_dir, exist_ok=True)

        for obj in scene.objects:
            if obj.type == 'MESH':
                base_name = obj.name.split('.')[0]

                model_matrix = {
                    "position": list(obj.location),
                    "rotation": list(obj.rotation_euler),
                    "scale": list(obj.scale)
                }

                tags = []
                if "tags" in obj.data:
                    tags = obj.data["tags"].split(',')

                texture_path = None
                if obj.data.materials:
                    for slot in obj.material_slots:
                        for node in slot.material.node_tree.nodes:
                            if node.type == 'TEX_IMAGE':
                                texture_path = "/sprites/" + node.image.filepath.split('/')[-1]
                                image_node = node
                                break
                        if texture_path is not None:
                            break

                output.append({
                    obj.name: {
                        "model_path": "/models/" + base_name + ".obj",
                        "texture_path": texture_path,
                        "model_matrix": model_matrix,
                        "tags": tags
                    }
                })

                # Export the mesh to an .obj file
                if base_name not in exported_meshes:
                    bpy.ops.object.select_all(action='DESELECT')
                    obj.select_set(True)

                    # Temporarily move the object to the origin
                    original_location = obj.location.copy()
                    obj.location = (0, 0, 0)

                    original_rotation = obj.rotation_euler.copy()
                    obj.rotation_euler = (0, 0, 0)


                    bpy.ops.export_scene.obj(filepath=os.path.join(models_dir, obj.name + ".obj"), use_selection=True)
                    exported_meshes.add(base_name)

                    # Move the object back to its original location
                    obj.location = original_location
                    obj.rotation_euler = original_rotation


                # If a texture image is found, copy it to the sprites folder
                if texture_path is not None:
                    # import shutil
                    # src_path = bpy.path.abspath(node.image.filepath)
                    # dst_path = os.path.join(sprites_dir, node.image.filepath.split('/')[-1])
                    # shutil.copy(src_path, dst_path)
                    image_node.image.file_format = 'PNG'
                    image_node.image.filepath_raw = os.path.join(sprites_dir, node.image.filepath.split('/')[-1])
                    image_node.image.save()

        with open(os.path.join(scenes_dir, scene_name), 'w') as f:
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