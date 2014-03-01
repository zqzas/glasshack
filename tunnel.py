import thread, json
from flask import request, session
from app import app
import urllib2

def render_id_cards(url):
    api = 'http://192.168.2.169:3000/misc/facematch'
    result = urllib2.urlopen(api + '?photo=' + url).read()
    session['user'].timeline.post(html=render_template(result))

def subscript(app, user):
    callbackUrl = 'https://mirrornotifications.appspot.com/forward?url=' + 'http://' + app.host
    print user.token
    print user.request("POST", "/mirror/v1/subscriptions", data=json.dumps({
        "collection": "timeline",
        "userToken": user.token,
#        "operation": ["INSERT"],
        "callbackUrl": "%s/share_callback" % callbackUrl,
      }))

if __name__ == '__main__':
    url = 'http://hooin.qiniudn.com/IMG_1497.JPG'
    process(url)
