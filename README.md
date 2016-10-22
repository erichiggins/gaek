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

When the encoder meets a property of the `ndb.Key` type, 
there are three encoding options available:   

* `ndb_keys_as_entities` - encode Key property as a `Future` whose eventual result is the entity for the key.
 This is the default option.
* `ndb_keys_as_pairs` - encode Key property as a tuple of (kind, id) pairs.
* `ndb_keys_as_urlsafe` - encode Key property as a websafe-base64-encoded serialized version of the key.

Please refer to [NDB Key Class](https://cloud.google.com/appengine/docs/python/ndb/keyclass) documentation for details.

For example, for the following data models:

```
    class Master(ndb.Model):
      name = ndb.StringProperty()
```
```
    class Details(ndb.Model):
      master = ndb.KeyProperty()
      description = ndb.StringProperty()
```

and following records:

```
    master = Master(id=123456L, name='Europe')
    details = Details(
      master=ndb.Key(Master, 123456L), 
      description='List of European customers'
     )
```

The calls
```
    json_str = ndb_json.dumps(details)
    json_str = ndb_json.dumps(details, ndb_keys_as_entities=True)
```
will return

```
{"master": {"name": "Europe"}, "description": "List of European customers"}
```

The call
```
    json_str = ndb_json.dumps(details, ndb_keys_as_pairs=True)
```
will return

```
{"master": [["Master", 123456]], "description": "List of European customers"}
```

The call
```
    json_str = ndb_json.dumps(details, ndb_keys_as_urlsafe=True)
```
will return

```
{"master": "agFfcg4LEgZNYXN0ZXIYwMQHDA", "description": "List of European customers"}
```


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


