from geometry import MusicBoxCylinder, Cylinder, Model
from mido import MidiFile
import note

radius = 50
height = 200

def createModel(midiFileName):
    cylinder = MusicBoxCylinder(0, 0, 0, radius, height)

    notes = note.getNotes(midiFileName, cylinder)

    model = Model('3D  Model', cylinder.shapes + notes)

    return model.create()
