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

    #------------------ORIGINAL
    r.lookAt(eye=[0,0,1],center=[0,0,0],up=[0,1,0])
    r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.05,0.05,0.05), rotate=(0,0,0), texture=t)
    
    #------------------MEDIUM SHOT
    #r.lookAt(eye=[0,0,1],center=[-5,0,0],up=[0,1,0])
    #r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.08,0.08,0.08), rotate=(0,0,0), texture=t)

    #------------------LOW ANGLE
    #r.lookAt(eye=[0,-0.5,1],center=[0,0,0],up=[0,1,0])
    #r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.06,0.06,0.06), rotate=(0,10,0), texture=t)
    
    #------------------HIGH ANGLE
    #r.lookAt(eye=[0,1,1],center=[0,0,0],up=[0,1,0])
    #r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.04,0.04,0.04), rotate=(0,10,0), texture=t)
    
    #------------------DUTCH ANGLE
    #r.lookAt(eye=[0,0,1],center=[0,0,0],up=[0,1,0])
    #r.glLoad('./models/apple.obj', translate=(-1,-1.5,0), scale=(0.055,0.055,0.055), rotate=(90,0,20), texture=t)

    r.glFinish()

glpoint()

