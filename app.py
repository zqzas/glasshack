# Python imports
from flask import request, session, render_template, redirect, url_for

# Import glass library
import glass

# Config imports
import config

app = glass.Application(
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    scopes=config.GOOGLE_SCOPES,
    template_folder="templates",
    static_url_path='/static',
    static_folder='static')

# Set the secret key for flask session.  keep this really secret: (but here it's not ;) )
app.web.secret_key = 's2Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.web.route("/")
def index():
    return render_template("index.html", auth=False)

@app.subscriptions.login
def login(user):
    print "google user: %s" % (user.token)
    session['token'] = user.token
    return "OK"

if __name__ == '__main__':
    print "Starting application at %s:%i" % (config.HOST, config.PORT)
    app.run(port=config.PORT, host=config.HOST)
    
