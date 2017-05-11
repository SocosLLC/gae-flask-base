# templating.py
#

from flask import get_flashed_messages, flash, jsonify, request
from flask import _app_ctx_stack
from flask.templating import _render
from flask.views import MethodView

import env_conf


# AJAX response handling ###########################################################################
# Pilfered from http://cam.st/ajax-block-rendering-in-flask/

def render_block(template, ctx, block=None):
    template_block = template.blocks.get(block)
    if not template_block:
        raise ValueError('Block {} does not exist in template {}.'.format(block, template.name))
    new_ctx = template.new_context(ctx)
    return ''.join(template_block(new_ctx))


class RenderView(MethodView):
    template_name = None
    base_template = 'layouts/base.html'
    container = '.view-container'
    block = 'view_container'
    title = None
    url = None

    def build_response(self, tmpl, context):
        return {
            'page': render_block(tmpl, ctx=context, block=self.block),
            'title': self.title,
            'url': self.url,
            'view_container': self.container,
            'pushState': True,
        }

    def render_template(self, **context):
        ctx = _app_ctx_stack.top
        ctx.app.update_template_context(context)
        jinja_env = ctx.app.jinja_env
        context.update({
            'content_template': self.template_name
        })
        template = jinja_env.get_or_select_template(self.template_name or self.base_template)
        if request.is_xhr:
            return jsonify(self.build_response(template, context))
        else:
            return _render(template, context, ctx.app)


