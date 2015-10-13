GAEK: Google App Engine Kit
===============================

[![Build Status](https://travis-ci.org/erichiggins/gaek.svg)](https://travis-ci.org/erichiggins/gaek)


A collection of useful tools for Python apps running on Google App Engine.

* Free software: BSD license
* Documentation: http://erichiggins.github.io/gaek/

NDB JSON module
---------------

Usage:

    from gaek import ndb_json

    # Serialize NDB Model(s) to a JSON string.
    json_str = ndb_json.dumps(models)

    # Parse a JSON string into a Python dictionary.
    ndb_json.loads(json_str)


Feature parity with the Python `json` module functions.

* `ndb_json.dumps`
* `ndb_json.dump`
* `ndb_json.loads`


Environment module
------------------

* `environ.get_dot_target_name(version=None, module=None)`

   Returns the current version/module in `-dot-` notation which is used by `target:` parameters.

* `environ.get_environ_dict()`

   Return a dictionary of all environment keys/values.

* `environ.is_host_google()`

   True if the app is being hosted from Google App Engine servers.

* `environ.is_development()`

   True if the dev_appserver is running (localhost or local development server).

* `environ.is_staging(version=None)`

   True if the app is hosted by Google (appspot.com) but the version is not the default.

* `environ.is_production(version=None)`

   True if the app is being hosted by Google and the default version.

* `environ.is_default_version(version=None)`

   True if the current or specified app version is the default.


