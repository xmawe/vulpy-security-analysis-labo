#!/usr/bin/env python3

from flask import Flask, g, redirect, request
import secrets

from mod_hello import mod_hello
from mod_user import mod_user
from mod_posts import mod_posts
from mod_mfa import mod_mfa

import libsession

app = Flask('vulpy')
# FIXED B105: Use secrets module instead of hardcoded key
app.config['SECRET_KEY'] = secrets.token_hex(32)

app.register_blueprint(mod_hello, url_prefix='/hello')
app.register_blueprint(mod_user, url_prefix='/user')
app.register_blueprint(mod_posts, url_prefix='/posts')
app.register_blueprint(mod_mfa, url_prefix='/mfa')


@app.route('/')
def do_home():
    return redirect('/posts')

@app.before_request
def before_request():
    g.session = libsession.load(request)

# FIXED B201: Removed debug=True for production security
app.run(debug=False, host='127.0.1.1', ssl_context=('/tmp/acme.cert', '/tmp/acme.key'))
