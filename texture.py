import struct 
from gl import *

def color(r, g, b):
  return bytes([b, g, r])

class Texture:
    def __init__(self):
        self.path = ''

    def read(self, path):
        self.path = path
        with open(self.path, "rb") as image:
            image.seek(2 + 4 + 4) 
            header_size = struct.unpack("=l", image.read(4))[0] 
            image.seek(2 + 4 + 4 + 4 + 4)
            
            self.width = struct.unpack("=l", image.read(4))[0]
            self.height = struct.unpack("=l", image.read(4))[0]

            image.seek(header_size)

            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))
                    self.pixels[y].append(color(r,g,b))

    def get_color(self, tx, ty, intensity=1):
        x = int(tx * self.width)
        y = int(ty * self.height)

        b = round(self.pixels[y][x][0]*intensity)
        g = round(self.pixels[y][x][1]*intensity)
        r = round(self.pixels[y][x][2]*intensity)

        try:
            if intensity > 0:
                return color(r,g,b)
            else:
                return self.pixels[y][x]
        except:
            pass
        
            
