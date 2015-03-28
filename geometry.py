class Vertex:
	_ID = 1

	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		
		self.id = self._ID 
		self.__class__._ID += 1

	def toString(self):
		return 'v %s %s %s' % (self.x, self.y, self.z)

class Face:
	def __init__(self, vertices = []):
		self.vertices = vertices

	def toString(self):
		objString = 'f'

		for vertex in self.vertices:
			objString += ' %s' % (vertex.id)

		return objString

