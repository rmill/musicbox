import cherrypy
import musicbox
import string
import random
import os, os.path

cherrypy.config.update('../config/server.conf')

FILE_STORAGE_PATH = '/var/run/musicbox'

class Index(object):
    @cherrypy.expose
    def index(self):
        #with open ("../view/index.html", "r") as myfile:
        with open ("../view/model.html", "r") as myfile:
            html = myfile.read()

        return html

    @cherrypy.expose
    def upload(self, myFile):
        # Read the MIDI file
        midiFile = ""
        while True:
            data = myFile.file.read(8192)
            if not data:
                break

            midiFile += data

        # Create a hash for the user's files
        fileHash = ''.join(random.choice(string.hexdigits) for i in range(24))

        # Save the MIDI file  to disk
        uploadFilePath = '%s/upload-%s.midi' % (FILE_STORAGE_PATH, fileHash)
        uploadFile = open(uploadFilePath, 'w')
        uploadFile.write(midiFile)
        uploadFile.close()

        # Create the 3D model
        model = musicbox.createModel(uploadFilePath)

        # Save the model to disk
        downloadFileName = 'download-%s.obj' % (fileHash)
        downloadFilePath =  '%s/%s' % (FILE_STORAGE_PATH, downloadFileName)
        downloadFile = open(downloadFilePath, 'w+')
        downloadFile.write(model)

        # Send the file to the user
        cherrypy.lib.static.serve_file(
            path=downloadFilePath,
            content_type='application/text',
            name=downloadFileName,
            disposition='attachment'
        )

if __name__ == '__main__':
    conf = {
         '/': {
             'tools.sessions.on': True,
             'tools.staticdir.root': os.path.abspath('/var/musicbox/')
         },
         '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': './public'
         }
     }

    cherrypy.quickstart(Index(), '/', conf)