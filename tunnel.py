import thread
from flask import request
import app

tl_ids = []

@app.app.subscriptions.action('SHARE')
def share(user):
    lst = user.timeline.list()
    print lst
    for tl in lst:
        if not tl['id'] in tl_ids:
            tl_ids.append(tl['id'])
            print tl
            #thread.start_new_thread(process, (tl['contentUrl'])

def process(url):
    pass

if __name__ == '__main__':
    pass
