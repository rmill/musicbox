from geometry import Face, Model, Shape, Vertex, Cylinder
from mido import MidiFile, MetaMessage
import math

DEFAULT_NOTE_DEPTH = 1
DEFAULT_NOTE_HEIGHT = 1
DEFAULT_NUMBER_OF_NOTES = 88.0
DEFAULT_TEMPO = 500000

def getNotes(midiFileName, cylinder):
    notes = []

    midifile = MidiFile(midiFileName)

    # Our current spot on the cylinder in degrees
    cursor = 0
    length = midifile.length
    degreesPerSecond = 360 / length

    # Create the note objects from the midi file
    for message in midifile:
        if 'time' in dir(message):
            if isinstance(message, MetaMessage):
                # MetaMessages distort the length of the song
                length -= message.time
                degreesPerSecond = 360 / length
            else:
                # Progress the cursor
                cursor -= message.time * degreesPerSecond

        if 'type' not in dir(message):
            continue

        if message.type == 'note_on' and message.velocity > 0:
            note = createNote(cursor, message.note, cylinder)
            notes.append(note)

    return notes

def createNote(degrees, note, cylinder, noteDepth=DEFAULT_NOTE_DEPTH, noteHeight=DEFAULT_NOTE_HEIGHT):

    noteWidth = cylinder.height / DEFAULT_NUMBER_OF_NOTES
    noteY = noteWidth * note

    # Create the vertex on the circle at the desired point
    radians = degrees * math.pi / 180
    z1 = math.sin(radians) * cylinder.radius
    x1 = math.cos(radians) * cylinder.radius
    vertex1 = Vertex(x1, noteY, z1)
    vertex5 = Vertex(x1, noteY + noteWidth, z1)

    # Create the vertex on the circle at the given width
    radians2 = radians - 2.0 * math.asin(noteDepth / (2.0 * cylinder.radius))
    z2 = math.sin(radians2) * cylinder.radius
    x2 = math.cos(radians2) * cylinder.radius
    vertex2 = Vertex(x2, noteY, z2)
    vertex6 = Vertex(x2, noteY + noteWidth, z2)

    vector = (x1 - x2, z1 - z2)
    magnitude = math.sqrt(pow(x1 - x2, 2) + pow(z1 - z2, 2))
    unitVector = (vector[0] / magnitude, vector[1] / magnitude)
    perpendicularVector = (unitVector[1], -unitVector[0])

    # Create the vertex of the bounding box at the desired point
    z3 = z1 + perpendicularVector[1] * noteHeight
    x3 = x1 + perpendicularVector[0] * noteHeight
    vertex3 = Vertex(x3, noteY, z3)
    vertex7 = Vertex(x3, noteY + noteWidth, z3)

    # Create the vertex of the bounding box at the given width
    z4 = z2 + perpendicularVector[1] * noteHeight
    x4 = x2 + perpendicularVector[0] * noteHeight
    vertex4 = Vertex(x4, noteY, z4)
    vertex8 = Vertex(x4, noteY + noteWidth, z4)

    face1 = Face([vertex1, vertex3, vertex7, vertex5])
    face2 = Face([vertex2, vertex4, vertex8, vertex6])
    face3 = Face([vertex3, vertex4, vertex8, vertex7])
    face4 = Face([vertex1, vertex2, vertex4, vertex3])
    face5 = Face([vertex5, vertex6, vertex8, vertex7])

    vertices = [vertex1, vertex2, vertex3, vertex4, vertex5, vertex6, vertex7, vertex8]
    faces = [face1, face2, face3, face4, face5]

    return Shape('Note', vertices, faces)
