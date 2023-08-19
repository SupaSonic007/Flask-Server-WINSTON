# TODO:
```md
Admin:
- Admin data fetch (js?)
- Admin pagination
- Admin inspection fix
- Control page
    - Interaction w/ Sam

Winstogram:
- Save to collection x
- Comments
- Likes (?)

Important for PyCon:
- Control page
    - Interaction w/ Sam
- Concurrent viewers (?)

Entire site
- Visualisation update
    - HTML, CSS

Wireless Data Transmitter

https://wireframe.cc/w8Q1UF
```

[Python Blender API Render](https://stackoverflow.com/questions/14982836/rendering-and-saving-images-through-blender-python)


```py
import bpy
import time

for i in range(100):
    time.sleep(0.05)
    bpy.context.scene.render.image_settings.file_format='JPEG'
    bpy.context.scene.render.filepath = 'D:/img.jpg'
    bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
    bpy.ops.transform.rotate(value=0.1, orient_axis='Z')
    with open("D:/img_written.txt", "w") as f:
        f.write("Writing")
    bpy.ops.render.render(use_viewport = True, write_still=True)
    with open("D:/img_written.txt", "w") as f:
        f.write("Written")
```

Fast_API, uvicorn

Pydantic