import thread
from flask import request

class Tunnel(object):
    def __init__(self, app):
        self.app = app

    @self.app.web.route('/tunnel')
    def send(self):
        img = request.args.get('img')
        thread.start_new_thread(self.callback, (img, ))
        return None

    def callback(self, img):
        pass

if __name__ == '__main__':
    t = Tunnel(None)
    t.send()
    print '1'
    while True:
        pass
