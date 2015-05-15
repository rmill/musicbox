#!/usr/bin/python

import musicbox
import sys

radius = 50
height = 200

try:
    midiFileName = sys.argv[1]
    outPutFileName = sys.argv[2]
except:
    print "Usage: python generate-model.py MIDI_FILE_NAME OUTPUT_FILE_NAME"
    exit()

print "Creating File: %s" % (outPutFileName)

model = musicbox.createModel(midiFileName)

outFile = open(outPutFileName, 'w')
outFile.write(model)
outFile.close()

print "Finished Creating File"
print "STAY GOLD"
