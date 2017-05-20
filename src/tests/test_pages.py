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

    def test_hello_in_browser(self):
        url = self.url_base()
        self.driver.get(url)
        self.wait_for_visibility_of_tag('body')
        body = self.driver.find_element_by_tag_name('body')
        self.assertIn('Hello', body.text)

    def test_ajaxy(self):
        url = self.url_base() + '/ajaxy?state=b'
        self.driver.get(url)
        email_input = self.driver.find_element_by_id('email')
        email_input.send_keys('a@b.com')
        submit_button = self.driver.find_element_by_id('email-form-submit')
        submit_button.click()
        a_btn = self.driver.find_element_by_id('a-btn')
        a_btn.click()
        self.wait_for_visibility_of('a')
        a_panel = self.driver.find_element_by_id('a')
        self.assertIn('a@b.com', a_panel.text)


