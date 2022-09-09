from texture import Texture
from gl import Render

def glpoint():
    r = Render()
    t = Texture()

    r.glCreateWindow(500,500)

    r.glClearColor(1,1,1) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,500,500) 

    r.glColor(1,1,1) #parametros en rango de 0 a 1

    t.read('./models/apple.bmp')
    r.active_texture = t
    r.active_shader = r.shader

    #------------------ORIGINAL
    r.lookAt(eye=[0,0,1],center=[0,0,0],up=[0,1,0])
    r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.05,0.05,0.05), rotate=(0,0,0), texture=t)

    r.draw('TRIANGLES')
    r.glFinish()

glpoint()

