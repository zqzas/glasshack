import thread, json
import config
from flask import request, session
from app import app
import urllib2
import requests

def render_id_cards(url):
    api = 'http://www.showks.cn:3000/misc/facematch'
    print url
    result = urllib2.urlopen(api + '?photo=' + url).read()
    print result
    #requests.post(config.SERVERURL + '/uploadhtml', result)
    #print 'upload done'
    return result
    

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
