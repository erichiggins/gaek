# -*- coding: utf-8 -*-

"""
test_environ
----------------------------------

Tests for `environ` module.
"""

import mock
import os
import unittest

from google.appengine.api import app_identity
from google.appengine.api import modules
from google.appengine.api import namespace_manager
from google.appengine.ext import testbed

from gaek import environ


__all__ = [
  'TestEnviron',
]


class TestEnviron(unittest.TestCase):

    def setUp(self):
        # Setups app engine test bed.
        # http://code.google.com/appengine/docs/python/tools/localunittesting.html
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Declare which service stubs you want to use.
        self.testbed.init_app_identity_stub()
        self.testbed.init_modules_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_app_identity_functions(self):
        assert app_identity.get_application_id == environ.get_application_id
        assert app_identity.get_default_version_hostname == environ.get_default_version_hostname
        assert app_identity.get_service_account_name == environ.get_service_account_name

    def test_modules_functions(self):
        assert modules.get_current_instance_id == environ.get_current_instance_id
        assert modules.get_current_module_name == environ.get_current_module_name
        assert modules.get_current_version_name == environ.get_current_version_name
        assert modules.get_default_version == environ.get_default_version
        assert modules.get_hostname == environ.get_hostname
        assert modules.get_modules == environ.get_modules
        assert modules.get_versions == environ.get_versions

    def test_namespace_functions(self):
        assert namespace_manager.get_namespace == environ.get_namespace
        assert namespace_manager.google_apps_namespace == environ.google_apps_namespace

    def test_get_environ_dict(self):
        # TODO(eric): This one is a bit hefty.
        pass

    def test_get_dot_target_name(self):
        val = environ.get_dot_target_name()
        assert val == 'testbed-version-dot-default', repr(val)

    def test_get_dot_target_name_safe(self):
        with mock.patch('gaek.environ.get_current_version_name_safe', return_value=None):
            val = environ.get_dot_target_name_safe()
            assert val is None, val
        with mock.patch('gaek.environ.get_current_module_name_safe', return_value=None):
            val = environ.get_dot_target_name_safe()
            assert val is None, val
        val = environ.get_dot_target_name_safe()
        assert val == 'testbed-version-dot-default', repr(val)

    def test_is_host_google(self):
        val = environ.is_host_google()
        assert val == False, repr(val)

    def test_is_development(self):
        val = environ.is_development()
        assert val == True, repr(val)

    def test_is_staging(self):
        val = environ.is_staging()
        assert val == False, repr(val)

    def test_is_staging_safe(self):
        with mock.patch('gaek.environ.get_current_version_name_safe', return_value=None):
            val = environ.is_staging_safe()
            assert val is False, repr(val)
        val = environ.is_staging_safe()
        assert val == False, repr(val)

    def test_is_production(self):
        val = environ.is_production()
        assert val == False, repr(val)

    def test_is_production_safe(self):
        with mock.patch('gaek.environ.get_current_version_name_safe', return_value=None):
            val = environ.is_production_safe()
            assert val is False, repr(val)
        val = environ.is_production_safe()
        assert val == False, repr(val)

    def test_is_default_version(self):
        val = environ.is_default_version()
        assert val == False, repr(val)

    def test_is_default_version_safe(self):
        with mock.patch('gaek.environ.get_current_version_name_safe', return_value=None):
            val = environ.is_default_version_safe()
        assert val == False, repr(val)

    def test_get_current_version_name_safe(self):
        # The version is stored in an environment variable 'CURRENT_VERSION_ID'.
        #  If that variable isn't present then an error will be raised unless we catch it.
        saved_version = os.environ.pop('CURRENT_VERSION_ID', None)

        version = 'v1'
        try:
            version = environ.get_current_version_name_safe()
        except Exception as err:
            self.fail('Unexpected exception when getting current version: {}'.format(
                err.message))
        assert version is None

        os.environ['CURRENT_VERSION_ID'] = saved_version

        # Now the environment variable is back.
        version = environ.get_current_version_name_safe()
        assert 'testbed-version' == version, version

    def test_get_current_module_name_safe(self):
        """
        Test that environ.get_current_module_name returns None when there is no
        current module, rather than raising an error.
        """
        # The current module is stored in an environment variable 'CURRENT_MODULE_ID'.
        saved_module_name = os.environ.pop('CURRENT_MODULE_ID', None)

        current_module = 'v1-app'
        try:
            current_module = environ.get_current_module_name_safe()
        except Exception as err:
            self.fail('Unexpected exception when getting current module: {}'.format(
                err.message))
        assert current_module is None

        os.environ['CURRENT_MODULE_ID'] = saved_module_name
        # Now the environment variable is back.
        current_module = environ.get_current_module_name_safe()
        assert 'default' == current_module, current_module


if __name__ == '__main__':
    unittest.main()
