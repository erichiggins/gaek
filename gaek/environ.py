# -*- coding: utf-8 -*-
"""
Environment discovery and helper functions for Google App Engine.
Some methods from the following modules have been made available for convenience:

* google.appengine.api.app_identity
  https://cloud.google.com/appengine/docs/python/appidentity/
* google.appengine.api.modules
  https://cloud.google.com/appengine/docs/python/modules/
* google.appengine.api.namespace_manager
  https://cloud.google.com/appengine/docs/python/multitenancy/

Example:

  import gaek.environ

  # Only send emails in production.
  if gaek.environ.is_production():
    mail.send(*args, **kwargs)
  
"""
 
__author__ = 'Eric Higgins'
__copyright__ = 'Copyright 2015, Eric Higgins'
__email__ = 'erichiggins@gmail.com'


import os

from google.appengine.api import app_identity
from google.appengine.api import modules
from google.appengine.api import namespace_manager


__all__ = (
    # App Identity functions.
    'get_application_id',
    'get_default_version_hostname',
    'get_service_account_name',
    # Module functions.
    'get_current_instance_id',
    'get_current_module_name',
    'get_current_version_name',
    'get_default_version',
    'get_hostname',
    'get_modules',
    'get_versions',
    # Namespace functions.
    'get_namespace',
    'google_apps_namespace',
    # Helper functions.
    'get_dot_target_name',
    'get_environ_dict',
    'is_host_google',
    'is_development',
    'is_staging',
    'is_production',
    'is_default_version',
)


_UNDEFINED = '_UNDEFINED_'


# App Identity functions.
get_application_id = app_identity.get_application_id
get_default_version_hostname = app_identity.get_default_version_hostname
get_service_account_name = app_identity.get_service_account_name


# Module functions.
get_current_instance_id = modules.get_current_instance_id
get_current_module_name = modules.get_current_module_name
get_current_version_name = modules.get_current_version_name
get_default_version = modules.get_default_version
get_hostname = modules.get_hostname
get_modules = modules.get_modules
get_versions = modules.get_versions


# Namespace functions.
get_namespace = namespace_manager.get_namespace
google_apps_namespace = namespace_manager.google_apps_namespace


# Helper functions.


def is_host_google():
  """True if the app is being hosted from Google App Engine servers."""
  return os.environ.get('SERVER_SOFTWARE', '').startswith('Google') or get_hostname().endswith('.appspot.com')


def is_default_version(version=None):
  """True if the current or specified app version is the default."""
  version = version or get_current_version_name()
  return version == get_default_version()


def is_development():
  """True if the dev_appserver is running (localhost or local development server)."""
  return os.environ.get('SERVER_SOFTWARE', '').startswith('Development')


def is_staging(version=None):
  """True if the app is hosted by Google (appspot.com) but the version is not the default."""
  return is_host_google() and not is_default_version(version)


def is_production(version=None):
  """True if the app is being hosted by Google and the default version."""
  return is_host_google() and is_default_version(version)


def get_dot_target_name(version=None, module=None):
  """Returns the current version/module in -dot- notation which is used by `target:` parameters."""
  version = version or get_current_version_name()
  module = module or get_current_module_name()
  return '-dot-'.join((version, module))


def _get_os_environ_dict(keys):
  """Return a dictionary of key/values from os.environ."""
  return {k: os.environ.get(k, _UNDEFINED) for k in keys}


def _get_app_identity_dict(keys):
  """Return a dictionary of key/values from the app_identity module functions."""
  return {k: getattr(app_identity, k)() for k in keys}


def _get_modules_dict(keys):
  """Return a dictionary of key/values from the modules module functions."""
  return {k: getattr(modules, k)() for k in keys}


def _get_namespace_manager_dict(keys):
  """Return a dictionary of key/values from the namespace_manager module functions."""
  return {k: getattr(namespace_manager, k)() for k in keys}


def get_environ_dict():
  """Return a dictionary of all environment keys/values."""
  return {
      'os.environ': _get_os_environ_dict((
          'AUTH_DOMAIN',
          'CURRENT_CONFIGURATION_VERSION',
          'CURRENT_MODULE_ID',
          'CURRENT_VERSION_ID',
          'DEFAULT_VERSION_HOSTNAME',
          'FEDERATED_IDENTITY',
          'FEDERATED_PROVIDER',
          'GAE_LOCAL_VM_RUNTIME',
          'HTTP_HOST',
          'HTTP_PROXY',
          'HTTP_X_APPENGINE_HTTPS',
          'HTTP_X_APPENGINE_QUEUENAME',
          'HTTP_X_ORIGINAL_HOST',
          'HTTP_X_ORIGINAL_SCHEME',
          'SERVER_NAME',
          'SERVER_PORT',
          'SERVER_SOFTWARE',
          'USER_IS_ADMIN',
      )),
      'app_identity': _get_app_identity_dict((
          'get_service_account_name',
          'get_application_id',
          'get_default_version_hostname',
      )),
      'modules': _get_modules_dict((
          'get_current_module_name',
          'get_current_version_name',
          'get_current_instance_id',
          'get_modules',
          'get_versions',
          'get_default_version',
          'get_hostname',
      )),
      'namespace_manager': _get_namespace_manager_dict((
          'get_namespace',
          'google_apps_namespace',
      )),
  }
