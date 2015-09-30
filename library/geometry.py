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

class Shape(object):
    def __init__(self, name = '', vertices = [], faces = []):
        self.name = name
        self.vertices = vertices
        self.faces = faces

    def addVertex(self, vertex):
        self.vertices.append(vertex)

    def addFace(self, face):
        self.faces.append(face)

    @staticmethod
    def createSkin(name, vertices1, vertices2):
        vertices = zip(vertices1, vertices2)
        skinFaces = []

        # Create the 'skin' of the two sets of vertices
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

        return Shape(name, vertices1 + vertices2, skinFaces)

class Model:
    def __init__(self, name = '', shapes = []):
        self.name = name
        self.shapes = shapes

    def create(self):
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

        return objString

class Circle(Shape):

    DEFAULT_RESOLUTION = 100

    def __init__(
        self,
        name,
        centerX,
        centerY,
        centerZ,
        radius,
        isOpen = False,
        resolution = DEFAULT_RESOLUTION
    ):
        self.name=name
        self.vertices=[]
        self.faces=[]
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.radius = radius
        self.isOpen = isOpen
        self.resolution = resolution
        self.shape = None

        self.render()

    def render(self):
        # Create the vertices
        for degrees in numpy.linspace(0, 360, self.resolution):
            z = math.sin(degrees * math.pi / 180) * self.radius
            x = math.cos(degrees * math.pi / 180) * self.radius

            vertex = Vertex(x, self.centerY, z)
            self.addVertex(vertex)

        # Create the face
        if not self.isOpen:
            self.addFace(Face(self.vertices))

class Cylinder():

    def __init__(self, centerX, centerY, centerZ, radius, height, isOpen = False):
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.radius = radius
        self.height = height
        self.isOpen = isOpen
        self.shapes = None

        self.render()

    def render(self):
        topCircle = Circle('Top Circle', 0, 0, 0, self.radius, isOpen=self.isOpen)
        bottomCircle = Circle('Bottom Circle', 0, self.height, 0, self.radius, isOpen=self.isOpen)
        skin = Shape.createSkin('Cylinder Skin', topCircle.vertices, bottomCircle.vertices)

        self.shapes = [topCircle, bottomCircle, skin]

    def getTopCircle(self):
        return self.shapes[0]

    def getBottomCircle(self):
        return self.shapes[1]

    def getSkin(self):
        return self.shapes[2]

class MusicBoxCylinder(Cylinder):

    def __init__(self, centerX, centerY, centerZ, radius, height):
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.radius = radius
        self.height = height
        self.shapes = None

        self.render()

    def render(self):
        outerCylinder = Cylinder(0, 0, 0, self.radius, self.height, isOpen=True)
        innerCylinder = Cylinder(0, 0, 0, 10, self.height, isOpen=True)

        topFaces = Shape.createSkin(
            'Top MusicBox Skin',
            outerCylinder.getTopCircle().vertices,
            innerCylinder.getTopCircle().vertices
        )

        bottomFaces = Shape.createSkin(
            'Bottom MusicBox Skin',
            outerCylinder.getBottomCircle().vertices,
            innerCylinder.getBottomCircle().vertices
        )

        self.shapes = outerCylinder.shapes + innerCylinder.shapes + [topFaces, bottomFaces]
