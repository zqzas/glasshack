import thread
from flask import request
import app
import urllib2

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
    api = 'http://192.168.2.169:3000/misc/facematch'
    result = urllib2.urlopen(api + '?photo=' + url).read()

if __name__ == '__main__':
    url = 'http://hooin.qiniudn.com/IMG_1497.JPG'
    process(url)
