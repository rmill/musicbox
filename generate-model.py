from geometry import Face, Model, Shape, Vertex
import math
import numpy

radius = 5
height = 15
resolution = 100

verticesTopCircle = []
verticesBottomCircle = []

# Create the vertices for the top and bottom circles of the cylinder
for degrees in numpy.linspace(0, 360, resolution):
    z = math.sin(degrees * math.pi / 180) * radius
    x = math.cos(degrees * math.pi / 180) * radius

    vertexTopCircle = Vertex(x, height, z)
    verticesTopCircle.append(vertexTopCircle)

    vertexBottomCircle = Vertex(x, 0, z)
    verticesBottomCircle.append(vertexBottomCircle)

    if z != 0:
        vertexTopCircle = Vertex(x, height, -z)
        verticesTopCircle.append(vertexTopCircle)
        
        vertexBottomCircle = Vertex(x, 0, -z)
        verticesBottomCircle.append(vertexBottomCircle)

facesTopCircle = [Face(verticesTopCircle)]
facesBottomCircle = [Face(verticesBottomCircle)]

shapeTopCircle = Shape('Top Circle', verticesTopCircle, facesTopCircle)
shapeBottomCircle = Shape('Bottom Circle', verticesBottomCircle, facesBottomCircle)

model = Model('3D  Model', [shapeTopCircle, shapeBottomCircle])

model.create()


def placeNote(degrees):
    noteHeight = 1
    noteWidth = 1

    note = Shape("Note")


    z1 = math.sin(degrees * math.pi / 180) * radius
    x1 = math.cos(degrees * math.pi / 180) * radius
    vertex1 = Vertex(x1, 0, z1)

    degrees2 = degrees - math.asin((noteWidth / 2.0) / radius)
    z2 = math.sin(degrees2) * radius
    x2 = math.cos(degrees2) * radius
    vertex1 = Vertex(x2, 0, z2)

    

placeNote(0)

