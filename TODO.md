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

<!-- e.g.

![Layout](https://tribe.so/wp-content/uploads/2021/06/social-media-site--1160x803.png)
![Layout](https://hasthemes.com/blog/wp-content/uploads/2022/01/Sociala-Social-Network-App-HTML-Template.png)
![Layout](https://cdn.dribbble.com/users/3082905/screenshots/17027157/social_media_app_-_nov_23__2021.png) -->
