from flask import Flask, Response, request, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os
import sys

basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')
# this should be append instead of insert...except for some reason that isn't working
sys.path.insert(1, basedir)
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import time
import random
from string import letters, digits
chars = letters + digits
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import models # MUST HAPPEN AFTER db is created above

# BROKEN DON'T USE YET
def create_and_send_email(send_to, api_key):
    # me == my email address
    # you == recipient's email address
    me = "do-not-reply@sleep-as-a-service"
    you = send_to

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Registration for Sleep as a Service"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    html = """\
    <html>
      <head></head>
      <body>
        <p>Welcome to Sleep as a Service!<br>

           You have been given a basic account - you can make 5000 requests
           per month.<br>

           Your API key is: %s<br>

           This is your API key - do not expose this key to external parties.
           <br>
        </p>

        <p>Request formats:<br>
            GET /sleep/&lt;seconds%gt;/&lt;api_key&gt;

            Seconds is expected to be an int from 1 to 60, inclusive.
        </p>
      </body>
    </html>
    """
    part = MIMEText(html, 'html')
    msg.attach(part)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, you, msg.as_string())
    s.quit()

@app.route('/')
def index():
    return render_template("index.html"), 200

@app.route('/register')
def register():
    key = ''.join(random.choice(chars) for _ in xrange(32))
    key = unicode(key)
    u = models.User(key=key, requests=5000)
    db.session.add(u)
    db.session.commit()
    return render_template("signup.html", key=key), 200

@app.route('/sleep/<int:ti>/<string:key>')
def sleep(ti, key):
    if ti > 60:
        return 'SaaS only supports sleeps up to a minute', 422
    user = models.User.query.filter_by(key=unicode(key)).first()
    if user is not None:
        time.sleep(ti)
        user.requests -= 1
        db.session.commit()
        return '', 200
    else:
        return '', 401

dev = False
host = '127.0.0.1' if dev else '0.0.0.0'
port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host=host, port=port)
