# ascii_scene_exporter
 Scene Exporter for my AsciiOpenglRust game engine


This plugin is very unintuitive to use, but it works.
I made it for my own use, but if you want to use it, you can.
Just dont blame me if it doesnt work for you.

Still i will write how it behaves.

first of all its a plugin for blender 2.8, so you need to install it.
Then you can find it in the export menu.

when you export you specify name for scene name and path is root folder of assets folder.

here is the structure of the exported files:

```
root_folder (you specify this)
├── models (this is where models are exported)
│   ├── ball.mtl
│   ├── ball.obj
│   ├── Cube.mtl
│   └── Cube.obj
├── scenes 
│   └── untitled.json (name of scene you put in export menu)
└── sprites (this is where sprites are exported)
    ├── ball.png
    └── Cube.png
```

names of models need to be unique, i made it that way so exporter wont export same model many times.

so for example my code treates "Cube" and "Cube.001" as same model, so it will export only one of them. Second will be added to json but it wont be exported to obj and mtl.

plugin will create folders if they dont exist. (to avoid errors / crashes)

currently model can have only one material, but i will try to add support for multiple materials in future.

and my plugin only reads for textures in base color slot, otherwise it will put null in json. Maybe i will add support for materials in future.

also i will try to add support for animations.

i will be expanding this plugin for my needs. So dont expect it to do everything.

if you have any questions, you can ask me on discord: `@f1l1p`