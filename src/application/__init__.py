# __init__.py
#

import os
import sys
import logging

import env_conf


# Initialize environment #######################################################

class Environment(object):
    DEV = False
    TEST = False
    STAGING = False
    PROD = False
    LOCAL = False  # True if DEV or TEST, false if STAGING or PROD
    env_name = None

    def __init__(self, mode):
        self.env_name = mode
        if mode == 'DEV':
            self.DEV = True
        elif mode == 'TEST':
            self.TEST = True
        elif mode == 'STAGING':
            self.STAGING = True
        elif mode == 'PROD':
            self.PROD = True
        else:
            raise ValueError('No such mode: {}'.format(mode))
        if self.DEV or self.TEST:
            self.LOCAL = True

_env_name = os.environ.get('ENV') or env_conf.FLASK_CONF

env = Environment(_env_name)


# Generic Initialization #######################################################

logging.basicConfig(stream=sys.stderr)

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import assets

app = Flask('application')
app.env = env

assets.init(app)

# Environment-specific initialization ##########################################

if app.env.DEV:
    print 'Environment: DEV'
    # Development settings
    app.config.from_object('application.settings.Development')
    # Flask-DebugToolbar
    toolbar = DebugToolbarExtension(app)

elif app.env.TEST:
    print 'Environment: TEST'
    app.config.from_object('application.settings.Testing')

elif app.env.STAGING:
    print 'Environment: STAGING'
    # Development settings
    app.config.from_object('application.settings.Staging')
    # Flask-DebugToolbar
    toolbar = DebugToolbarExtension(app)

else:
    assert app.env.PROD
    print 'Environment: PROD'
    app.config.from_object('application.settings.Production')


# Jinja2 Configuration ########################################################

# Loop controls extension
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# Better debugging
if app.env.LOCAL:
    from google.appengine.tools.devappserver2.python import sandbox
    sandbox._WHITE_LIST_C_MODULES += ['_ctypes', 'gestalt']


# Pull in URL dispatch routes #################################################

import urls
