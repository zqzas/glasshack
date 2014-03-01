# Python imports
from flask import request, session, render_template, redirect, url_for

# Import glass library
import glass

# Config imports
import config

#import tunnel
import urllib2

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

appProfile = {  'displayName' : 'gFace', 
                'id' : 'gFace_0.1', 
                'imageUrls' : [config.ADDRESS + '/static/logo.jpg'], 
                'acceptTypes' : ['image/jpeg', 'image/png']
             }

# Set the secret key for flask session.  keep this really secret: (but here it's not ;) )
app.web.secret_key = 's2Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.web.route('/share_callback')
def share():
    print 'fuckyou'
    lst = userObj.timeline.list()
    print lst
    for tl in lst:
        if not tl['id'] in tl_ids:
	    global tl_ids
            tl_ids.append(tl['id'])
            print tl
            url = 'http://hooin.qiniudn.com/IMG_1497.JPG'
            #thread.start_new_thread(render_id_cards, url)# (tl['contentUrl'])

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
    
