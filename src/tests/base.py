# base.py
#

from collections import Counter
import inspect
import logging
import os
from pprint import pprint
import unittest
import urllib

from flask_testing import TestCase
from wsgi_liveserver import LiveServerTestCase
from google.appengine.ext import ndb, testbed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver, WebElement
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchElementException, TimeoutException,
                                        ElementNotVisibleException)

import application

# Make sure we don't collide with the dev server
LiveServerTestCase.port_range = (9080, 9090)

# Nose provides a handler that we want to reduce the verbosity of
LOG = logging.getLogger('').handlers[0]
LOG.setFormatter(logging.Formatter(unicode(logging.BASIC_FORMAT)))
LOG.setLevel(logging.INFO)

QUICK = os.environ.get('QUICK') == '1'

QUIET = os.environ.get('QUIET') == '1'


####################################################################################################
# Test Base for NoseGAE web tests

class TestBase(TestCase):
    # Remove the ones you don't need
    nosegae_app_identity_service = True
    nosegae_blobstore = True
    nosegae_datastore_v3 = True
    nosegae_mail = True
    nosegae_memcache = True
    nosegae_logservice = True
    nosegae_user = True
    nosegae_urlfetch = True

    def create_app(self):
        # Flask apps testing. See: http://flask.pocoo.org/docs/testing/
        application.app.config['TESTING'] = True
        application.app.config['WTF_CSRF_ENABLED'] = False
        return application.app

    def setUp(self):
        self.client = application.app.test_client()

    ################################################################################################
    # Utility functions

    def assert_radio_selection_is(self, soup, expected_value):
        selected_device = soup.find('input', type='radio', checked=True)
        self.assertIsNotNone(selected_device, 'No radio selection has been made')
        if expected_value:
            self.assertEqual(selected_device.get('value'), expected_value)
        else:
            self.assertIsNone(selected_device)

    def assert_select_selection_is(self, soup, select_id, expected_value):
        select = soup.find('select', id=select_id)
        selected = select.find('option', selected=True).get('value').strip()
        self.assertEqual(selected, expected_value)

    def assert_redirect_path(self, rv, expected_path):
        self.assertEqual(rv.location.split('/')[-1], expected_path)

    def client_get(self, path, query_params=(), *args, **kwargs):
        """
        A wrapper for self.client.get that parses query_param_data into a
        query_params string.
        """
        query_string = urllib.urlencode(query_params)
        return self.client.get(path, *args, query_string=query_string, **kwargs)

    def client_post(self, path, query_params=(), *args, **kwargs):
        """
        A wrapper for self.client.post that parses query_param_data into a
        query_params string.
        """
        query_string = urllib.urlencode(query_params)
        return self.client.post(path, *args, query_string=query_string, **kwargs)


####################################################################################################
# Test Base for Selenium tests

class LiveServerTestBase(LiveServerTestCase):
    # Remove the ones you don't need
    nosegae_app_identity_service = True
    nosegae_blobstore = True
    nosegae_datastore_v3 = True
    nosegae_mail = True
    nosegae_memcache = True
    nosegae_logservice = True
    nosegae_user = True
    nosegae_urlfetch = True

    def create_app(self):
        context = ndb.get_context()
        context.set_cache_policy(False)
        context.set_memcache_policy(False)
        return application.app

    def setUp(self):
        # self.driver = self._firefox_webdriver()  # Uncomment to use firefox
        self.driver = self._phantomjs_webdriver()  # Comment out to use firefox
        # self._tear_down()  # uncomment to clean up crap

    def _firefox_webdriver(self):
        return webdriver.Firefox()

    def _phantomjs_webdriver(self):
        driver = webdriver.PhantomJS(service_log_path='tmp/ghostdriver.log',
                                     service_args=['--load-images=false',
                                                   '--ignore-ssl-errors=true',
                                                   '--ssl-protocol=TLSv1'])
        driver.set_window_size(1920, 1080)
        return driver

    def _tear_down(self):
        self.driver.close()
        self.driver.quit()

    def tearDown(self):
        self._tear_down()

    def output_debug(self):
        if not QUIET:
            print 'CONSOLE'
            pprint(self.console())
            print 'SOURCE'
            print self.driver.page_source
            self.save_screenshot()

    def console(self):
        return self.driver.get_log('browser')

    # Keep track of what screenshot number we're on for each test, for save_screenshot
    _screenshot_call_counts = Counter()

    def save_screenshot(self):
        class_name = self.__class__.__name__
        stack = inspect.stack()
        stack_functions = []
        test_name = None
        for i in range(1, 6):
            fcn_name = stack[i][3]
            if fcn_name.startswith('test'):
                test_name = fcn_name
                break
            else:
                stack_functions.append(fcn_name)
        test_name = test_name or stack[1][3]
        count_key = class_name + '-' + test_name
        count = self.__class__._screenshot_call_counts[count_key]
        self.__class__._screenshot_call_counts.update([count_key])
        file_name = 'tmp/{}-{}-{}{}.png'.format(class_name, test_name, count,
                                                ''.join(['-' + n for n in stack_functions]))
        self.driver.save_screenshot(file_name)

    # Testing Stuff ################################################################################

    def assert_element_id_exists(self, id_, driver=None):
        self._assert_element_exists('id', id_, driver=driver)

    def assert_element_class_exists(self, class_, driver=None):
        self._assert_element_exists('class_name', class_, driver=driver)

    def assert_element_name_exists(self, name, driver=None):
        self._assert_element_exists('name', name, driver=driver)

    def _assert_element_exists(self, identifier_type, identifier, driver=None):
        driver = driver or self.driver
        try:
            find_fcn = getattr(driver, 'find_element_by_' + identifier_type)
            find_fcn(identifier)
        except NoSuchElementException:
            if isinstance(driver, WebElement) and not QUIET:
                print 'FAILED ON ELEMENT'
                print driver.get_attribute('innerHTML')
            self.save_screenshot()
            self.fail('No element with {} {} found'.format(identifier_type, identifier))

    def assert_element_id_does_not_exist(self, id_, driver=None):
        self._assert_element_does_not_exist('id', id_, driver=driver)

    def assert_element_class_does_not_exist(self, class_, driver=None):
        self._assert_element_does_not_exist('class', class_, driver=driver)

    def _assert_element_does_not_exist(self, identifier_type, identifier, driver=None):
        driver = driver or self.driver
        try:
            find_fcn = getattr(driver, 'find_element_by_' + identifier_type)
            find_fcn(identifier)
            if not QUIET:
                print 'FAILED ON ELEMENT'
                self.output_debug()
            self.fail('Element with {} {} found'.format(identifier_type, identifier))
        except NoSuchElementException:
            pass

    def assert_select_is(self, element_id, expected_text=None, expected_value=None, driver=None):
        driver = driver or self.driver
        select = Select(driver.find_element_by_id(element_id))
        selected_option = select.first_selected_option  # type: WebElement
        if not QUIET:
            self.output_debug()
        if expected_value:
            self.assertEqual(selected_option.get_attribute('value').strip(), expected_value)
        else:
            self.assertEqual(selected_option.text.strip(), expected_text)

    # Driver Support ###############################################################################

    def print_source(self, driver_or_element=None):
        driver_or_element = driver_or_element or self.driver
        if isinstance(driver_or_element, WebDriver):
            print driver_or_element.page_source
        elif isinstance(driver_or_element, WebElement):
            print driver_or_element.get_attribute('outerHTML')
        else:
            raise NotImplementedError('Unknown type {}'.format(driver_or_element.__class__.__name__))

    def stub_js_confirm(self):
        """ PhantomJS doesn't support alert boxes. This stubs out the
            window.confirm function to immediately return true. """
        script = "window.confirm = function(msg) { return true; }"
        self.driver.execute_script(script);

    def wait_for(self, element_id, driver=None):
        return self._wait_for(element_id, status='presence', identifier_type='ID', driver=driver)

    def wait_for_visibility_of(self, element_id, driver=None):
        return self._wait_for(element_id, driver=driver)

    def wait_for_invisibility_of(self, element_id, driver=None):
        return self._wait_for(element_id, status='invisibility',
                              identifier_type='ID', driver=driver)

    def wait_for_visibility_of_class(self, element_class, driver=None):
        return self._wait_for(element_class, status='visibility',
                              identifier_type='CLASS_NAME', driver=driver)

    def wait_for_invisibility_of_class(self, element_class, driver=None):
        return self._wait_for(element_class, status='invisibility',
                              identifier_type='CLASS_NAME', driver=driver)

    def wait_for_visibility_of_tag(self, element_tag, driver=None):
        return self._wait_for(element_tag, status='visibility',
                              identifier_type='TAG_NAME', driver=driver)

    def _wait_for(self, identifier, status='visibility', identifier_type='ID', driver=None):
        driver = driver or self.driver
        try:
            status_fcn = getattr(EC, status + '_of_element_located')
            by = getattr(By, identifier_type)
            WebDriverWait(driver, 6).until(
                status_fcn((by, identifier))
            )
        except TimeoutException, e:
            if not QUIET:
                print 'FAILED ON ELEMENT'
                self.output_debug()
            e.msg = '{} {} never got {}.'.format(identifier_type, identifier, status)
            raise e

    def wait_for_text_in_element(self, element_id, text, driver=None):
        driver = driver or self.driver
        try:
            WebDriverWait(driver, 6).until(
                EC.text_to_be_present_in_element((By.ID, element_id), text)
            )
        except TimeoutException, e:
            print 'FAILED ON ELEMENT'
            self.output_debug()
            e.msg = 'Text {} never showed up.'.format(text)
            raise e

