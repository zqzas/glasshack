import thread
from flask import request, session
from app import app
import urllib2

tl_ids = []

@app.web.route('/callback')
def share(user):
    lst = user.timeline.list()
    print lst
    for tl in lst:
        if not tl['id'] in tl_ids:
            tl_ids.append(tl['id'])
            print tl
            url = 'http://hooin.qiniudn.com/IMG_1497.JPG'
            #thread.start_new_thread(render_id_cards, url)# (tl['contentUrl'])

def render_id_cards(url):
    api = 'http://192.168.2.169:3000/misc/facematch'
    result = urllib2.urlopen(api + '?photo=' + url).read()
    session['user'].timeline.post(html=render_template(result))

def subscrip(user):
    user.request("POST", "/mirror/v1/subscriptions", data=json.dumps({
        "collection": "timeline",
        "userToken": user.token,
        "operation": "INSERT",
        "callbackUrl": "%s/callback" % self.app.host,
      }))

if __name__ == '__main__':
    url = 'http://hooin.qiniudn.com/IMG_1497.JPG'
    process(url)
