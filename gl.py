# ===============================================================
# Gráficas Por Computadora
# Stefano Aragoni - 20261
# ===============================================================

from logging import raiseExceptions
from collections import namedtuple
import struct

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
        f.write(self.pixels[x][y])

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
    if not (-1 <= x <= 1) or not (-1 <= y <= 1):
      raise Exception('Coordenada invalida. Ingrese valores entre -1 y 1.')

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

  def triangle(self, v1, v2, v3, color_ = None, texture=None, texture_coords=(), intensity=1):

    min, max = bounding_box([v1.x, v2.x, v3.x],[v1.y, v2.y, v3.y])

    for x in range(min.x, max.x+1):
      for y in range(min.y, max.y+1):
        w, v, u = barycentric(v1.x, v1.y, v2.x, v2.y, v3.x, v3.y, x, y)

        if w < 0 or v < 0 or u < 0: 
          continue

        self.current_color = color_

        if texture:
          tA, tB, tC = texture_coords
          tx = (tA.x * w) + (tB.x * v) + (tC.x * u)
          ty = (tA.y * w) + (tB.y * v) + (tC.y * u)
          
          self.current_color = texture.get_color_with_intensity(tx, ty, intensity)

        z = (v1.z * w) + (v2.z * v) + (v3.z * u)

        x_temp, y_temp = x/self.width, y/self.height
        
        tempx = int(self.x2 + (self.width2/2) + (x_temp * self.width2/2))
        tempy = int(self.y2 + (self.height2/2) + (-y_temp * self.height2/2))
      
        if z > self.zbuffer[tempx][tempy]:
          self.zbuffer[tempx][tempy] = z
          self.glVertex(x_temp, y_temp)

  def transform_vertex(self, vertex, scale, translate):
    return V3(
      round((vertex[0] + translate[0]) * scale[0]),
      round((vertex[1] + translate[1]) * scale[1]),
      round((vertex[2] + translate[2]) * scale[2]),
    )
    
  def glLoad(self, filename, translate=(0,0,0), scale=(1,1,1), texture=None):
    archivo = Obj(filename)
    light = V3(0,0,1)
    
    for face in archivo.faces:
      vcount = len(face)

      if vcount == 3:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1], scale, translate)
        v2 = self.transform_vertex(archivo.vertex[f2], scale, translate)
        v3 = self.transform_vertex(archivo.vertex[f3], scale, translate)

        normal = norm(cross(sub(v2, v1), sub(v3, v1)))
        intensity = dot(normal, light)

        if not texture:
          if intensity < 0:
            continue  

          self.triangle(v1, v2, v3, color(intensity, intensity, intensity))

        else:
          f12 = face[0][1] - 1
          f22 = face[1][1] - 1
          f32 = face[2][1] - 1
          
          t1 = V3(*archivo.tvertex[f12])
          t2 = V3(*archivo.tvertex[f22])
          t3 = V3(*archivo.tvertex[f32])

          self.triangle(v2, v1, v3, texture=texture, texture_coords=(t1, t3, t2), intensity=intensity)
          
      if vcount == 4:
        f1 = face[0][0] - 1
        f2 = face[1][0] - 1
        f3 = face[2][0] - 1
        f4 = face[3][0] - 1

        v1 = self.transform_vertex(archivo.vertex[f1], scale, translate)
        v2 = self.transform_vertex(archivo.vertex[f2], scale, translate)
        v3 = self.transform_vertex(archivo.vertex[f3], scale, translate)
        v4 = self.transform_vertex(archivo.vertex[f4], scale, translate)

        normal = norm(cross(sub(v1, v2), sub(v2, v3)))
        intensity = dot(normal, light)

        if not texture:
          if intensity < 0:
            continue  

          self.triangle(v1, v3, v2, color(intensity, intensity, intensity))
          self.triangle(v1, v4, v3, color(intensity, intensity, intensity))
          
        else:
          f12 = face[0][1] - 1
          f22 = face[1][1] - 1
          f32 = face[2][1] - 1
          f42 = face[3][1] - 1

          t1 = V3(*archivo.tvertex[f12])
          t2 = V3(*archivo.tvertex[f22])
          t3 = V3(*archivo.tvertex[f32])
          t4 = V3(*archivo.tvertex[f42])
          
          self.triangle(v1, v3, v2, texture=texture, texture_coords=(t1, t3, t2), intensity=intensity)
          self.triangle(v1, v4, v3, texture=texture, texture_coords=(t1, t4, t3), intensity=intensity)
