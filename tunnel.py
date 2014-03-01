import thread, json
from flask import request, session
from app import app
import urllib2

def get_img_url(user, itemid, attachment_id):
    r = user.request("GET", "https://www.googleapis.com/mirror/v1/timeline/%s/attachments/%s" % (itemid, attachment_id))
    print r
    return json.loads(r)['contentUrl']

@app.web.route('/share_callback')
def share():
    print 'fuckyou'
    lst = userObj.timeline.list()
    print lst
    for tl in lst:
        if not tl['id'] in tl_ids:
            global tl_ids
            tl_ids.append(tl['id'])
            url = get_img_url(userObj, tl['id'], tl['attachments']['id'])
            thread.start_new_thread(render_id_cards, url)

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
