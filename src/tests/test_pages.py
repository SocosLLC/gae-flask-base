# -*- coding: utf-8 -*-
#
# test_pages.py
#

import unittest

from bs4 import BeautifulSoup

import base


class TestEndpoints(base.TestBase):

    def test_thing(self):
        rv = self.client.get('/')
        soup = BeautifulSoup(rv.data, 'lxml')
        self.assert200(rv)
        self.assertIn('Hello', soup.find('body').get_text())


class TestInBrowser(base.LiveServerTestBase):

    def test_message_sends(self):
        url = self.url_base()
        self.driver.get(url)
        self.wait_for_visibility_of_tag('body')
        body = self.driver.find_element_by_tag('body')
        self.assertIn('Hello', body)
