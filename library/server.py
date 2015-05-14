import cherrypy
import musicbox
import string
import random

cherrypy.config.update('../config/server.conf')

class Index(object):
    @cherrypy.expose
    def index(self):
        with open ("../view/index.html", "r") as myfile:
            html = myfile.read()

        return html

    @cherrypy.expose
    def upload(self, myFile):
        midiFile = ""
        while True:
            data = myFile.file.read(8192)
            if not data:
                break

            midiFile += data

        fileHash = ''.join(random.choice(string.hexdigits) for i in range(24))

        uploadFileName = 'upload-%s.midi' % (fileHash)
        uploadFile = open(uploadFileName, 'w')
        uploadFile.write(midiFile)
        uploadFile.close()

        model = musicbox.createModel(uploadFileName)

        downloadFileName = 'download-%s.obj' % (fileHash)
        downloadFile = open(downloadFileName, 'w+')
        downloadFile.write(model)

        return cherrypy.lib.static.serve_file(
            path='/var/musicbox/library/%s' % (downloadFileName),
            content_type='application/text',
            name=downloadFileName,
            disposition='attachment'
        )

if __name__ == '__main__':
    cherrypy.quickstart(Index())