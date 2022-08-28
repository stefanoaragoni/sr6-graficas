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

    #r.lookAt((100,100,100),(0,0,0),(0,0,0))

    t.read('./models/apple.bmp')
    #r.glLoad('./models/rock.obj', (0,-200,0), (1,1,1),(0,0,0), t)
    r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(0,90,0), t)
    
    r.glFinish()

glpoint()

