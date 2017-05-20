#
# handlers.py
#

import logging

from flask import flash, render_template, request

from application import forms, models, templating

LOG = logging.getLogger(__name__)


def warmup():
    return ''


def home():
    return render_template('home.html')


class AjaxyView(templating.RenderView):

    template_name = 'ajaxy/main.html'
    container = '#ajaxy-panel'
    block = 'ajaxy_content'
    title = 'Ajaxy Account'
    url = '/ajaxy'

    def get(self):
        LOG.info(request.args)
        state = request.args.get('state') or 'a'
        return self.render_page(state=state)

    def post(self):
        form = forms.EmailForm(request.form)
        email = form.email.data
        entry = models.Email.query(models.Email.email == email).get()
        if entry:
            flash('Email already exists!', 'info')
            return self.render_page(state='b', form=form)
        else:
            new_entry = models.Email(email=email)
            new_entry.put()
        return self.render_page(state='b')

    def render_page(self, state, form=None):
        if state == 'b':
            form = form or forms.EmailForm()
            return self.render_template(state=state, form=form)
        else:
            email_entities = models.Email.query().fetch()
            emails = [e.email for e in email_entities]
            return self.render_template(state=state, emails=emails)

