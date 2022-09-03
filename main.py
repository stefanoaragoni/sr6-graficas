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

    t.read('./models/model.bmp')
    r.lookAt(eye=[1,0,1],center=[0,0,0],up=[0,1,0])

    #------------------ORIGINAL
    r.glLoad('./models/model.obj', translate=(0,-2,0), scale=(0.5,0.5,0.5), rotate=(0,0,0), texture=t)
    
    #------------------MEDIUM SHOT
    #r.glLoad('./models/apple.obj', (-250,-50,0), (5,5,5),(0,0,0), t)
    #r.glLoad('./models/apple.obj', (250,-50,0), (5,5,5),(0,180,0), t)

    #------------------LOW ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(100,-10,0), t)

    #------------------HIGH ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(95,0,0), t)

    #------------------DUTCH ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(90,0,20), t)

    


    r.glFinish()

glpoint()

