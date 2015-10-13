GAEK: Google App Engine Kit
===============================

[![Build Status](https://travis-ci.org/erichiggins/gaek.svg)](https://travis-ci.org/erichiggins/gaek)


A collection of useful tools for Python apps running on Google App Engine.

* Free software: BSD license
* Documentation: https://gaek.readthedocs.org.

NDB JSON module
---------------

Usage:

    from gaek import ndb_json

    # Serialize NDB Model(s) to a JSON string.
    json_str = ndb_json.dumps(models)

    # Parse a JSON string into a Python dictionary.
    ndb_json.loads(json_str)


Feature parity with the Python `json` module functions.

`ndb_json.dumps`

`ndb_json.dump`

`ndb_json.loads`


Environment module
------------------

Usage:

    from gaek import environ


API:

