from geometry import Face, Vertex
import math
import numpy

radius = 5
height = 15
resolution = 10

verticesTopCircle = []
verticesBottomCircle = []

# Create the vertices for the top and bottom circles of the cylinder
for x in numpy.linspace(-radius, radius, (resolution + 2) / 2):
	z = math.sqrt(radius**2 - x**2)

	vertexTopCircle = Vertex(x, height, z)
	verticesTopCircle.append(vertexTopCircle)

	vertexBottomCircle = Vertex(x, 0, z)
	verticesBottomCircle.append(vertexBottomCircle)

	if z != 0:
		vertexTopCircle = Vertex(x, height, -z)
		verticesTopCircle.append(vertexTopCircle)
		
		vertexBottomCircle = Vertex(x, 0, -z)
		verticesBottomCircle.append(vertexBottomCircle)

faceTopCircle = Face(verticesTopCircle)
faceBottomCircle = Face(verticesBottomCircle)

# Create the OBJ file
fileObject = open('test.obj', 'w')

fileObject.write('# Top Cicle Vertices\n')
for vertex in verticesTopCircle:
	fileObject.write(vertex.toString() + '\n')
	
fileObject.write('\n# Bottom Cicle Vertices\n')
for vertex in verticesBottomCircle:
	fileObject.write(vertex.toString() + '\n')

fileObject.write('\n# Top Circle Face\n')
fileObject.write(faceTopCircle.toString() + '\n')

fileObject.write('\n# Bottom Circle Face\n')
fileObject.write(faceBottomCircle.toString() + '\n')

fileObject.close()
