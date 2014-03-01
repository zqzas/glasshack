import thread
from flask import request
import app

tl_ids = []

def get_image(tl):
     #r = self.user.request("GET", "/mirror/v1/timeline/", data = {})
     print tl

@app.app.subscriptions.action('SHARE')
def share(user):
    for tl in user.timeline.list():
        if not tl['id'] in tl_ids:
            tl_ids.append(tl)
            img = get_image(tl['id'])
            #thread.start_new_thread(process, (img, ))

def display_card():
    pass

def process(img):
    display_card()

if __name__ == '__main__':
    pass
