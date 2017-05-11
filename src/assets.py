#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# assets.py
#
"""
Makes assets ready for the browser.
"""

import os
import shutil
from flask import Flask
from flask_assets import Bundle, Environment

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'application', 'assets')
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'application', 'static')


def init(app=None):
    app = app or Flask(__name__)
    bundles = []

    with app.app_context():
        env = Environment(app)
        env.load_path = [ASSETS_DIR]
        env.set_directory(STATIC_DIR)
        # App Engine doesn't support automatic rebuilding.
        env.auto_build = False
        # This file needs to be shipped with your code.
        env.manifest = 'file'
        bundles.extend(_add_base_bundle(env))
        bundles.extend(_add_home_bundle(env))
        bundles.extend(_add_ajaxy_bundle(env))

    return bundles


def _add_base_bundle(env):
    css = Bundle(
        "src/css/base.css",
        "src/css/footer.css",
        filters=["autoprefixer6", "cssmin"], output="css/base.min.css")
    env.register('base_css', css)

    libs_css = Bundle(
        "libs/bootstrap/dist/css/bootstrap.css",
        filters=["cssmin"], output="css/base-libs.min.css")
    env.register('base_libs_css', libs_css)

    js = Bundle(
        "src/js/ajaxHandler.js",
        filters="jsmin", output="js/base.min.js")
    env.register('base_js', js)

    libs_js = Bundle(
        "libs/jquery/dist/jquery.js",
        "libs/bootstrap/dist/js/bootstrap.js",
        filters="jsmin", output="js/base-libs.min.js")
    env.register('base_libs_js', libs_js)

    return css, libs_css, js, libs_js


def _add_home_bundle(env):
    css = Bundle(
        "src/css/home.css",
        filters=["autoprefixer6", "cssmin"], output="css/home.min.css")
    env.register('home_css', css)

    return css,


def _add_ajaxy_bundle(env):
    css = Bundle(
        "src/css/ajaxy.css",
        filters=["autoprefixer6", "cssmin"], output="css/ajaxy.min.css")
    env.register('ajaxy_css', css)

    js = Bundle(
        "src/js/ajaxy.js",
        filters="jsmin", output="js/ajaxy.min.js")
    env.register('ajaxy_js', js)

    return css, js


# From http://stackoverflow.com/a/12514470/1464495
def _copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


if __name__ == '__main__':
    print 'Building asset bundles'
    bundles = init()
    for bundle in bundles:
        bundle.build()
    print 'Copying fonts into static/'
    bootstrap_fonts_dir = os.path.join(ASSETS_DIR, 'libs', 'bootstrap', 'fonts')
    target_fonts_dir = os.path.join(STATIC_DIR, 'fonts')
    if not os.path.exists(target_fonts_dir):
        os.makedirs(target_fonts_dir)
    _copytree(bootstrap_fonts_dir, target_fonts_dir)

