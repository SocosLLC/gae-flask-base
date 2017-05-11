#
# urls.py
#

from flask import render_template

from application import app, handlers


# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=handlers.warmup)

# Home page
app.add_url_rule('/', view_func=handlers.home)

# Ajaxy page
app.add_url_rule('/ajaxy', view_func=handlers.AjaxyView.as_view('ajaxy'))


####################################################################################################
# Error handlers

# Handle 403 errors
@app.errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

