# Python imports
from flask import request, session, render_template, redirect, url_for

# Import glass library
import glass

# Config imports
import config

import urllib2, json, thread

import tunnel

app = glass.Application(
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    scopes=config.GOOGLE_SCOPES,
    template_folder="templates",
    static_url_path='/static',
    static_folder='static')

userTokens = {}
userObj = None
tl_ids = []

appProfile = {  'displayName' : 'gFace', 
                'id' : 'gFace_0.1', 
                'imageUrls' : [config.ADDRESS + '/static/logo.jpg'], 
                'acceptTypes' : ['image/jpeg', 'image/png']
             }

# Set the secret key for flask session.  keep this really secret: (but here it's not ;) )
app.web.secret_key = 's2Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def get_img_url(user, itemid, attachment_id):
    r = user.request("GET", "https://www.googleapis.com/mirror/v1/timeline/%s/attachments/%s" % (itemid, attachment_id))
    print r, r.json()
    imgUrl = str(r.json()['contentUrl'])
    locImgPath = '/srv/www/zqzas.com/public_html/static/%s.jpeg' % (itemid)
     
    import os.path
    if os.path.isfile(locImgPath):
        print 'Duplication: ', itemid
        return False
    print 'Ready to get ', imgUrl

    r = user.request("GET", imgUrl)
    print 'Fetch finished' , '---' * 10
           
    f = open(locImgPath , 'wb')
    f.write(r.content)
    f.flush()
    f.close()
    return 'http://zqzas.com' + '/' + 'static/%s.jpeg' % itemid


@app.web.route('/share_callback')
def share():
    print 'callback here'
    lst = userObj.timeline.list()
    #print lst
    global tl_ids
    print 'list got'
    for tl in lst:
    	print tl
    	if not 'attachments' in tl:
	    continue
    	if len(tl['attachments']) <= 0:
	    continue
    
    	url = get_img_url(userObj, tl['id'], tl['attachments'][0]['id'])
    	if not url:
	    continue
    	print 'rendering'
    	html = tunnel.render_id_cards(url)

	print html
        uploadHtml(html)
	return html
    return "STILL WAITING FOR ACTIVITY"


def uploadHtml(html):
    data = html
    print data
    userObj.timeline.post(html = data)
    

@app.web.route("/")
def index():
    return render_template("index.html", auth=False)


#@app.web.route("/posttestcard")
#def postTestCard():
#    print render_template("card.html")
#    session['user'].timeline.post(html=render_template("card.html"))
#    print "POST OK"
#    return "OK"

def insertContact(user):
    print 'getting contacts list'
    contacts = user.contacts.list()
    for contact in contacts:
        if contact['displayName'] == appProfile['displayName']:
            print 'deleting existing contact'
            user.contacts.delete(contact['id'])
    print 'inserting contact'
    user.contacts.insert(displayName = appProfile['displayName'], id = appProfile['id'], imageUrls = appProfile['imageUrls'], acceptTypes = appProfile['acceptTypes'])
    print 'inserting done'

@app.subscriptions.login
def login(user):
    print "google user: %s" % (user.token)
    session['token'] = user.token
    session['user'] = user
    global userObj
    userObj = user
    #postTestCard()
    userTokens = user.tokens
    print 'start inserting contact'
    # insertContact(user)
    print 'contact added: ', appProfile
    tunnel.subscript(app, user)
    # return redirect('/')



if __name__ == '__main__':
    print "Starting application at %s:%i" % (config.HOST, config.PORT)
    app.run(port=config.PORT, host=config.HOST, debug=True)
	
    
