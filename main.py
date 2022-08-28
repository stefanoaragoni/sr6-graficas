from texture import Texture
from gl import Render

def glpoint():
    r = Render()
    t = Texture()

    r.glCreateWindow(500,500)

    r.glClearColor(0,0,0) #parametros en rango de 0 a 1
    r.glClear()

    r.glViewPort(0,0,500,500) 

    r.glColor(1,1,1) #parametros en rango de 0 a 1

    t.read('./models/octo.bmp')
    r.glLoad('./models/octo.obj', (0,0,0), (150,150,150), t)

    r.glFinish()

glpoint()

