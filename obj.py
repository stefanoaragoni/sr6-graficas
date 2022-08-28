class Obj(object):
  def __init__(self, filename):
    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.vertex = []  #v
    self.faces = [] #f
    self.tvertex = [] #tv

    for line in self.lines:
      line = line.strip()
      if line:
        prefix, value = line.split(' ', 1)

        if prefix == 'v':
          temp = value.split(' ')
          tempArray = []

          for tempValue in temp:
            tempArray.append((float(tempValue)))

          self.vertex.append(tempArray)

        elif prefix == 'vt':
          temp = value.split(' ')
          tempArray = []

          for tempValue in temp:
            tempArray.append((float(tempValue)))

          if(len(tempArray)==2):
            tempArray.append(0)
            
          self.tvertex.append(tempArray)

          
        elif prefix == 'f':
          temp = value.split(' ')
          tempArray = []
          
          for tempValue in temp:
            temp2 = tempValue.split('/')
            tempArray2 = []

            for tempValue2 in temp2:
              tempArray2.append((int(tempValue2)))

            tempArray.append(tempArray2)
          
          self.faces.append(tempArray)
  