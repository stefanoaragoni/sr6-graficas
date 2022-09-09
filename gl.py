# ===============================================================
# Gráficas Por Computadora
# Stefano Aragoni - 20261
# ===============================================================

from logging import raiseExceptions
from collections import namedtuple
import struct
from math import *

from texture import *
from obj import *
from matrixmath import *

# ========== Tamaños =========

def char(c):
  return struct.pack('=c', c.encode('ascii'))

def word(w):
  return struct.pack('=h', w)

def dword(d):
  return struct.pack('=l', d)

def color(r, g, b):
  return bytes([int(b*255), int(g*255), int(r*255)])

# ========== VECTOR =========
V3 = namedtuple('P3', ['x', 'y', 'z'])


def sum(v0, v1):
  return V3(v0.x + v1.x, v0.y + v1.y, v0.z + v1.z)

def sub(v0, v1):
  return V3(v0.x - v1.x, v0.y - v1.y, v0.z - v1.z)

def mul(v0, k):
  return V3(v0.x * k, v0.y * k, v0.z *k)

def dot(v0, v1):
  return v0.x * v1.x + v0.y * v1.y + v0.z * v1.z

def cross(v0, v1):
  return V3(
    v0.y * v1.z - v0.z * v1.y,
    v0.z * v1.x - v0.x * v1.z,
    v0.x * v1.y - v0.y * v1.x,
  )

def length(v0):
  return (v0.x**2 + v0.y**2 + v0.z**2)**0.5

def norm(v0):
  v0length = length(v0)

  if not v0length:
    return V3(0, 0, 0)

  return V3(v0.x/v0length, v0.y/v0length, v0.z/v0length)

# ========== Utils =========

def bounding_box(x, y):
  x.sort()
  y.sort()

  return V3(x[0], y[0], 0), V3(x[-1], y[-1], 0)

def barycentric(x1, y1, x2, y2, x3, y3, x4, y4):

  c = cross(
    V3(x2 - x1, x3 - x1, x1 - x4), 
    V3(y2 - y1, y3 - y1, y1 - y4)
  )

  if c.z == 0:
    return -1, -1, -1

  return (c.x / c.z, c.y / c.z, 1 - ((c.x + c.y) / c.z))

# ========== Colores =========

BLACK = color(0, 0, 0)
WHITE = color(1, 1, 1)

# ========== Render =========

class Render(object):
  def __init__(self):
    self.current_color = BLACK
    self.background_color = WHITE
    self.Model = None

    self.vertex_buffer_object = []
    self.active_vertex_array = []
    self.active_texture = None
    self.active_shader = None
    self.light = V3(0,0,1)

  def loadModelMatrix(self, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0)):
    translate = V3(*translate)
    scale = V3(*scale)
    rotate = V3(*rotate)

    transition_matrix = [
      [1, 0, 0, translate.x],
      [0, 1, 0, translate.y],
      [0, 0, 1, translate.z],
      [0, 0, 0, 1]
    ]

    scale_matrix = [
      [scale.x, 0, 0, 0],
      [0, scale.y, 0, 0],
      [0, 0, scale.z, 0],
      [0, 0, 0, 1]
    ]

    a = rotate.x
    rotation_x = [
      [1, 0, 0, 0],
      [0, cos(a), -sin(a), 0],
      [0, sin(a), cos(a), 0],
      [0, 0, 0, 1]
    ]

    a = rotate.y
    rotation_y = [
      [cos(a), 0, sin(a), 0],
      [0, 1, 0, 0],
      [-sin(a), 0,  cos(a), 0],
      [0, 0, 0, 1]
    ]

    a = rotate.z
    rotation_z = [
      [cos(a), -sin(a), 0, 0],
      [sin(a), cos(a), 0, 0],
      [0, 0, 1, 0],
      [0, 0, 0, 1]
    ]

    first = mult(rotation_x,rotation_y)
    rotation_matrix = mult(first,rotation_z)

    second = mult(transition_matrix,rotation_matrix)
    self.Model = mult(second,scale_matrix)

  def loadViewMatrix(self, x, y, z, center):
    Mi = [
      [x.x, x.y, x.z, 0],
      [y.x, y.y, y.z, 0],
      [z.x, z.y, z.z, 0],
      [0, 0, 0, 1]
    ]

    Op = [
      [1, 0, 0, -center.x],
      [0, 1, 0, -center.y],
      [0, 0, 1, -center.z],
      [0, 0, 0, 1]
    ]

    self.View = mult(Mi, Op)

  def loadProjectionMatrix(self, coeff):
    self.Projection = [
      [1, 0, 0, 0],
      [0, 1, 0, 0],
      [0, 0, 1, 0],
      [0, 0, -0.001, 1]
    ]

  def loadViewportMatrix(self):
    w = self.width2/4
    h = self.height2/4

    self.Viewport = [
      [w, 0, 0, w],
      [0, h, 0, h],
      [0, 0, 128, 128],
      [0, 0, 0, 1]
    ]

  def lookAt(self, eye, center, up):
    eye = V3(*eye)
    center = V3(*center)
    up = V3(*up)

    z = norm(sub(eye,center))
    x = norm(cross(up, z))
    y = norm(cross(z, x))

    self.loadViewMatrix(x, y, z, center)
    self.loadProjectionMatrix(-1 / length(sub(eye, center)))
    self.loadViewportMatrix()

  def glCreateWindow(self, width=100, height=100):
    self.width = width
    self.height = height
    self.inc = 1/height

  def glViewPort(self, x=0, y=0, width=99, height=99):
    self.width2 = width-1
    self.height2 = height-1
    self.x2 = x
    self.y2 = y

  def glClear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)] 
      for y in range(self.height)
    ]

    self.zbuffer = [
			[-99999 for x in range(self.width)]
			for y in range(self.height)
		]

  def glColor(self, r, g, b):
    if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
      raise Exception('Color RGB invalido. Ingrese valores entre 0 y 1.')

    self.current_color = color(r, g, b)

  def glClearColor(self, r, g, b):
    if not (0 <= r <= 1) or not (0 <= g <= 1) or not (0 <= b <= 1):
      raise Exception('Color RGB invalido. Ingrese valores entre 0 y 1.')
    self.background_color = color(r, g, b)

  def glFinish(self):
    f = open('out.bmp', 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for y in range(self.height-1, -1, -1):
      for x in range(self.width):
        try:
          f.write(self.pixels[x][y])
        except:
          f.write(BLACK)

    f.close()

  def glFinishZbuffer(self):
    f = open('zbuffer.bmp', 'bw')

    # File header (14 bytes)
    f.write(char('B'))
    f.write(char('M'))
    f.write(dword(14 + 40 + self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(14 + 40))

    # Image header (40 bytes)
    f.write(dword(40))
    f.write(dword(self.width))
    f.write(dword(self.height))
    f.write(word(1))
    f.write(word(24))
    f.write(dword(0))
    f.write(dword(self.width * self.height * 3))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))
    f.write(dword(0))

    for y in range(self.height-1, -1, -1):
      for x in range(self.width):
        try:
          f.write(color(self.zbuffer[x][y]/255,self.zbuffer[x][y]/255,self.zbuffer[x][y]/255))
        except:
          f.write(color(0,0,0))

    f.close()

  def glVertex(self, x, y):
    try:
      X0 = int(self.x2 + (self.width2/2) + (x * self.width2/2))
      Y0 = int(self.y2 + (self.height2/2) + (-y * self.height2/2))
      self.pixels[X0][Y0] = self.current_color
      
    except:
      pass

  def glLine(self, x0, y0, x1, y1):

    if not (-1 <= x0 <= 1) or not (-1 <= y0 <= 1) or not (-1 <= x1 <= 1) or not (-1 <= y1 <= 1):
      raise Exception('Coordenada invalida. Ingrese valores entre -1 y 1.')
        
    pendiente = abs(y1 - y0) > abs(x1 - x0) 

    if (pendiente):
      x0, y0 = y0, x0
      x1, y1 = y1, x1

    if x0 > x1:
      x0, x1 = x1, x0
      y0, y1 = y1, y0

    dy, dx = abs(y1 - y0), abs(x1 - x0)
    y, x = y0, x0

    offdy, offdx = 0, dx

    while (x < x1):
      offdy += dy * 2

      #creacion de puntos
      if pendiente:
        self.glVertex(y, x)
      else:
        self.glVertex(x, y)

      #incrementa/reduce Y conforme pasitos proporcionales
      if offdy >= offdx:
        if y < y1:
          y += self.inc #self.inc se calcula al crear el Window
        else:
          y -= self.inc
          
        offdx += dx * 2
      
      #incrementa X conforme pasitos proporcionales
      x += self.inc

  def shader(self, **kwargs):
    w, u, v = kwargs['bar']
    L = kwargs['light']
    A, B, C = kwargs['vertices']
    tA, tB, tC = kwargs['texture_coords']
    nA, nB, nC = kwargs['normals']

    iA = dot(norm(nA),norm(L))
    iB = dot(norm(nB),norm(L))
    iC = dot(norm(nC),norm(L))

    i = iA * w + iB * u + iC * v  

    if self.active_texture:
        tx = tA.x * w + tB.x * u + tC.x * v
        ty = tA.y * w + tB.y * u + tC.y * v

        return self.active_texture.get_color_with_intensity(tx, ty, i)
  
  def triangle(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
        tB = next(self.active_vertex_array)
        tA = next(self.active_vertex_array)
        tC = next(self.active_vertex_array)
        
    if self.active_shader:
        nB = next(self.active_vertex_array)
        nA = next(self.active_vertex_array)
        nC = next(self.active_vertex_array)

  ############################# CALCULOS #############################

    min, max = bounding_box([A.x, B.x, C.x],[A.y, B.y, C.y])

    for x in range(min.x, max.x+1):
      for y in range(min.y, max.y+1):
        w, v, u = barycentric(A.x, A.y, B.x, B.y, C.x, C.y, x, y)

        if w < 0 or v < 0 or u < 0: 
          continue

        z = (A.z * w) + (B.z * v) + (C.z * u)

        x_temp, y_temp = x/self.width, y/self.height
        
        tempx = int(self.x2 + (self.width2/2) + (x_temp * self.width2/2))
        tempy = int(self.y2 + (self.height2/2) + (-y_temp * self.height2/2))
      
        ############################# DIBUJO #############################
        try:
          if tempx >= 0 and tempy >= 0 and z > self.zbuffer[tempx][tempy]:
          
            self.zbuffer[tempx][tempy] = z

            self.current_color = self.active_shader(
              bar = (w,u,v),
              vertices=(A,B,C),
              texture_coords = (tA,tB,tC),
              normals = (nA,nB,nC),
              light = self.light
            )
            self.glVertex(x_temp,y_temp)
        except:
          pass


  def wireframe(self):
    A = next(self.active_vertex_array)
    B = next(self.active_vertex_array)
    C = next(self.active_vertex_array)

    if self.active_texture:
      tA = next(self.active_vertex_array)
      tB = next(self.active_vertex_array)
      tC = next(self.active_vertex_array)
    
    self.glLine(A.x, A.y,B.x, B.y)
    self.glLine(B.x, B.y,C.x, C.y)
    self.glLine(C.x, C.y,A.x, A.y)

  def transform_vertex(self, vertex):
    augmented_vertex = [
      vertex[0],
      vertex[1],
      vertex[2],
      1
    ]

    matrix1 = multmv(self.Model, augmented_vertex)
    matrix2 = multmv(self.View, matrix1)
    matrix3 = multmv(self.Projection, matrix2)
    transformed_vertex = multmv(self.Viewport, matrix3)

    return V3(
      round(transformed_vertex[0] / transformed_vertex[3]),
      round(transformed_vertex[1] / transformed_vertex[3]),
      round(transformed_vertex[2] / transformed_vertex[3]),
    )

  def glLoad(self, filename, translate=(0,0,0), scale=(1,1,1), rotate=(0,0,0), texture=None):
    archivo = Obj(filename)
    light = self.light

    self.loadModelMatrix(translate, scale, rotate)
     
    ############################# FOR #############################

    for face in archivo.faces:
      vcount = len(face)

      ############################# VCOUNT 3 #############################

      if vcount == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1])
        v2 = self.transform_vertex(archivo.vertex[f2])
        v3 = self.transform_vertex(archivo.vertex[f3])

        self.vertex_buffer_object.append(v1)
        self.vertex_buffer_object.append(v2)
        self.vertex_buffer_object.append(v3)

        if self.active_texture:
          ft1 = face[0][1] - 1
          ft2 = face[1][1] - 1
          ft3 = face[2][1] - 1

          vt1 = V3(*archivo.tvertex[ft1])
          vt2 = V3(*archivo.tvertex[ft2])
          vt3 = V3(*archivo.tvertex[ft3])

          self.vertex_buffer_object.append(vt1)
          self.vertex_buffer_object.append(vt2)
          self.vertex_buffer_object.append(vt3)

        try:
          fn1 = face[0][2] - 1
          fn2 = face[1][2] - 1
          fn3 = face[2][2] - 1

          vn1 = V3(*archivo.nvertex[fn1])
          vn2 = V3(*archivo.nvertex[fn2])
          vn3 = V3(*archivo.nvertex[fn3])
      
          self.vertex_buffer_object.append(vn1)
          self.vertex_buffer_object.append(vn2)
          self.vertex_buffer_object.append(vn3)
        except:
          pass
          
      ############################# VCOUNT 4 #############################

      if vcount == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1])
        v2 = self.transform_vertex(archivo.vertex[f2])
        v3 = self.transform_vertex(archivo.vertex[f3])
        v4 = self.transform_vertex(archivo.vertex[f4])
        
        self.vertex_buffer_object.append(v1)
        self.vertex_buffer_object.append(v2)
        self.vertex_buffer_object.append(v3)
        
        if self.active_texture:

            ft1 = face[0][1] - 1
            ft2 = face[1][1] - 1
            ft3 = face[2][1] - 1

            vt1 = V3(*archivo.tvertex[ft1])
            vt2 = V3(*archivo.tvertex[ft2])
            vt3 = V3(*archivo.tvertex[ft3])

            self.vertex_buffer_object.append(vt1)
            self.vertex_buffer_object.append(vt2)
            self.vertex_buffer_object.append(vt3)

        try:
            fn1 = face[0][2] - 1
            fn2 = face[1][2] - 1
            fn3 = face[2][2] - 1

            vn1 = V3(*archivo.nvertex[fn1])
            vn2 = V3(*archivo.nvertex[fn2])
            vn3 = V3(*archivo.nvertex[fn3])
        
            self.vertex_buffer_object.append(vn1)
            self.vertex_buffer_object.append(vn2)
            self.vertex_buffer_object.append(vn3)
        except:
            pass

        self.vertex_buffer_object.append(v1)
        self.vertex_buffer_object.append(v3)
        self.vertex_buffer_object.append(v4)

        if self.active_texture:

            ft1 = face[0][1] - 1
            ft3 = face[2][1] - 1
            ft4 = face[3][1] - 1

            vt1 = V3(*archivo.tvertex[ft1])
            vt3 = V3(*archivo.tvertex[ft3])
            vt4 = V3(*archivo.tvertex[ft4])

            self.vertex_buffer_object.append(vt1)
            self.vertex_buffer_object.append(vt3)
            self.vertex_buffer_object.append(vt4)
        try:
            fn1 = face[0][2] - 1
            fn3 = face[2][2] - 1
            fn4 = face[3][2] - 1

            vn1 = V3(*archivo.nvertex[fn1])
            vn3 = V3(*archivo.nvertex[fn3])
            vn4 = V3(*archivo.nvertex[fn4])
        
            self.vertex_buffer_object.append(vn1)
            self.vertex_buffer_object.append(vn3)
            self.vertex_buffer_object.append(vn4)
        except:
            pass


    self.active_vertex_array = iter(self.vertex_buffer_object)

  def draw(self,polygon):
    if polygon == 'TRIANGLES':
        try:
            while True:
                self.triangle()
        except StopIteration:
            print("terminado")
    if polygon == 'WIREFRAME':
        try:
            while True:
                self.wireframe()
        except StopIteration:
            print("terminado")