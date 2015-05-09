import numpy
import math

class Vertex:
    _ID = 1

    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

        self.id = self._ID
        self.__class__._ID += 1

class Face:
    def __init__(self, vertices = []):
        self.vertices = vertices

class Shape:
    def __init__(self, name = '', vertices = [], faces = []):
        self.name = name
        self.vertices = vertices
        self.faces = faces

    def addVertex(vertex):
        self.vertices.append(vertex)

    def addFace(face):
        self.faces.append(vertex)

class Model:
    def __init__(self, name = '', shapes = []):
        self.name = name
        self.shapes = shapes

    def create(self, fileName):
        # Create the OBJ file
        objString = ''
        currentVertexIndex = 1
        vertexIndex = {}

        for shape in self.shapes:
            objString += '# %s\n' % (shape.name)

            for vertex in shape.vertices:
                # Only print a vertex once
                if vertex.id in vertexIndex:
                   continue

                vertexIndex[vertex.id] = currentVertexIndex
                currentVertexIndex += 1
                objString += 'v %s %s %s\n' % (vertex.x, vertex.y, vertex.z)

            for face in shape.faces:
                faceString = 'f'

                for vertex in face.vertices:
                    faceString += ' %s' % (vertexIndex[vertex.id])

                objString += '%s\n' % (faceString)

            objString += '\n'

        fileObject = open(fileName, 'w')
        fileObject.write(objString)
        fileObject.close()

class Circle(Shape):

    DEFAULT_RESOLUTION = 100

    def __init__(self, centerX, centerY, centerZ, radius, resolution = DEFAULT_RESOLUTION):
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.radius = radius
        self.resolution = resolution
        self.shape = None

        self.render()

    def render(self):
        vertices = []

        # Create the vertices
        for degrees in numpy.linspace(0, 360, self.resolution):
            z = math.sin(degrees * math.pi / 180) * self.radius
            x = math.cos(degrees * math.pi / 180) * self.radius

            vertex = Vertex(x, self.centerY, z)
            vertices.append(vertex)

        # Create the face
        faces = [Face(vertices)]

        self.shape = Shape('Circle', vertices, faces)

class Cylinder():

        def __init__(self, centerX, centerY, centerZ, radius, height):
            self.centerX = centerX
            self.centerY = centerY
            self.centerZ = centerZ
            self.radius = radius
            self.height = height
            self.shapes = None

            self.render()

        def render(self):
            topCircle = Circle(0, 0, 0, self.radius)
            bottomCircle = Circle(0, self.height, 0, self.radius)

            topCircleVertices = topCircle.shape.vertices
            bottomCircleVertices = bottomCircle.shape.vertices

            vertices = zip(topCircleVertices, bottomCircleVertices)
            skinFaces = []

            # Create the 'skin' of the cylinder
            for index, value in enumerate(vertices):
                nextIndex = (index + 1) % len(vertices)

                sliverVertices = [
                    vertices[index][0],
                    vertices[index][1],
                    vertices[nextIndex][1],
                    vertices[nextIndex][0]
                ]

                face = Face(sliverVertices)
                skinFaces.append(face)

            skin = Shape('Cylinder Skin', topCircleVertices + bottomCircleVertices, skinFaces)

            self.shapes = [topCircle.shape, bottomCircle.shape, skin]
