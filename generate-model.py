from geometry import Face, Model, Shape, Vertex, Cylinder
from mido import MidiFile
import sys

radius = 5
height = 15

def main():
    cylinder = Cylinder(0, 0, 0, radius, height)
    
    #try:
    #    midiFileName = sys.argv[1]
    #except:
    #    print "Usage: python generate-model.py MIDI_FILE_NAME"
    #    exit()

    #notes = getNotes(midiFileName)
    notes = []

    model = Model('3D  Model', cylinder.shapes + notes)

    model.create()

def getNotes(midiFileName):
    try:
        MidiFile(midiFileName)
    except:
        print "File '%s' not found" % midiFileName
        exit()

def createNote(degrees):
    noteHeight = 1
    noteWidth = 1
    noteDepth = 2

    radians = degrees * math.pi / 180

    # Create the vertex on the circle at the desired point
    z1 = math.sin(radians) * radius
    x1 = math.cos(radians) * radius
    vertex1 = Vertex(x1, 0, z1)
    vertex5 = Vertex(x1, noteDepth, z1)

    # Create the vertex on the circle at the given width
    radians2 = radians - 2.0 * math.asin(noteWidth / (2.0 * radius))
    z2 = math.sin(radians2) * radius
    x2 = math.cos(radians2) * radius
    vertex2 = Vertex(x2, 0, z2)
    vertex6 = Vertex(x2, noteDepth, z2)

    vector = (x1 - x2, z1 - z2)
    magnitude = math.sqrt(pow(x1 - x2, 2) + pow(z1 - z2, 2))
    unitVector = (vector[0] / magnitude, vector[1] / magnitude)
    perpendicularVector = (unitVector[1], -unitVector[0])

    # Create the vertex of the bounding box at the desired point
    z3 = z1 + perpendicularVector[1] * noteHeight
    x3 = x1 + perpendicularVector[0] * noteHeight
    vertex3 = Vertex(x3, 0, z3)
    vertex7 = Vertex(x3, noteDepth, z3)

    # Create the vertex of the bounding box at the given width
    z4 = z2 + perpendicularVector[1] * noteHeight
    x4 = x2 + perpendicularVector[0] * noteHeight
    vertex4 = Vertex(x4, 0, z4)
    vertex8 = Vertex(x4, noteDepth, z4)

    face1 = Face([vertex1, vertex3, vertex7, vertex5])
    face2 = Face([vertex2, vertex4, vertex8, vertex6])
    face3 = Face([vertex3, vertex4, vertex8, vertex7]) 
    face4 = Face([vertex1, vertex2, vertex4, vertex3])
    face5 = Face([vertex5, vertex6, vertex8, vertex7])
    
    vertices = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7, vertex8]
    faces = [face1, face2, face3, face4, face5]

    return Shape('Note', vertices, faces)

main()

