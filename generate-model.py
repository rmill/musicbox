from geometry import Cylinder, Model
from mido import MidiFile
import sys
import note

radius = 5
height = 15

try:
    midiFileName = sys.argv[1]
except:
    print "Usage: python generate-model.py MIDI_FILE_NAME"
    exit()

cylinder = Cylinder(0, 0, 0, radius, height)

notes = note.getNotes(midiFileName)

model = Model('3D  Model', cylinder.shapes + notes)

model.create()
