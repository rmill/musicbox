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

	def create(self):
		# Create the OBJ file
		objString = ''
		currentVertexIndex = 1

		for shape in self.shapes:
			vertexIndex = {}

			objString += '# %s\n' % (shape.name)

			for vertex in shape.vertices:
				vertexIndex[vertex.id] = currentVertexIndex
				currentVertexIndex += 1 
				objString += 'v %s %s %s\n' % (vertex.x, vertex.y, vertex.z)

			for face in shape.faces:
				faceString = 'f'
				
				for vertex in shape.vertices:
					faceString += ' %s' % (vertexIndex[vertex.id])

				objString += '%s\n' % (faceString)

			objString += '\n'

		fileObject = open('test.obj', 'w')
		fileObject.write(objString)
		fileObject.close()


