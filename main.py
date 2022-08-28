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
    #t.read('./models/rock.bmp')
    #r.glLoad('./models/rock.obj', (0,-200,0), (1,1,1),(0,0,0), t)

    t.read('./models/apple.bmp')

    #------------------ORIGINAL
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(0,0,0), t)
    
    #------------------MEDIUM SHOT
    r.glLoad('./models/apple.obj', (-250,-50,0), (5,5,5),(0,0,0), t)
    r.glLoad('./models/apple.obj', (250,-50,0), (5,5,5),(0,180,0), t)

    #------------------LOW ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(100,-10,0), t)

    #------------------HIGH ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(95,0,0), t)

    #------------------DUTCH ANGLE
    #r.glLoad('./models/apple.obj', (0,-50,0), (7,7,7),(90,0,20), t)

    


    r.glFinish()

glpoint()

