# -*- coding: utf-8 -*-
"""
JSON encoder/decoder adapted for use with Google App Engine NDB.

Usage:

  import ndb_json

  # Serialize an ndb.Query into an array of JSON objects.
  query = models.MyModel.query()
  query_json = ndb_json.dumps(query)

  # Convert into a list of Python dictionaries.
  query_dicts = ndb_json.loads(query_json)

  # Serialize an ndb.Model instance into a JSON object.
  entity = query.get()
  entity_json = ndb_json.dumps(entity)

  # Convert into a Python dictionary.
  entity_dict = ndb_json.loads(entity_json)


Dependencies:

  - dateutil: https://pypi.python.org/pypi/python-dateutil
"""

__author__ = 'Eric Higgins'
__copyright__ = 'Copyright 2013-2016, Eric Higgins'
__email__ = 'erichiggins@gmail.com'


import base64
import datetime
import json
import re
import time
import types

import arrow
import dateutil.parser
from google.appengine.ext import ndb


__all__ = (
    'dump',
    'dumps',
    'loads',
    'NdbDecoder',
    'NdbEncoder',
)


DATE_RE = re.compile(r'\d{4}[-/]\d{2}[-/]\d{2}')


def encode_model(obj):
  """Encode objects like ndb.Model which have a `.to_dict()` method."""
  obj_dict = obj.to_dict()
  for key, val in obj_dict.iteritems():
    if isinstance(val, types.StringType):
      try:
        unicode(val)
      except UnicodeDecodeError:
        # Encode binary strings (blobs) to base64.
        obj_dict[key] = base64.b64encode(val)
  return obj_dict


def encode_generator(obj):
  """Encode generator-like objects, such as ndb.Query."""
  return list(obj)


def encode_key_as_entity(obj):
  """Get the Entity from the ndb.Key for further encoding."""
  # NOTE(erichiggins): Potentially poor performance for Models w/ many KeyProperty properties.
  # NOTE(ronufryk): Potentially can cause circular references and "RuntimeError: maximum recursion depth exceeded"
  return obj.get_async()


# Alias for backward-compatibility
encode_key = encode_key_as_entity


def encode_key_as_pair(obj):
  """Get the ndb.Key as a tuple of (kind, id) pairs."""
  return obj.pairs()


def encode_key_as_urlsafe(obj):
  """Get the ndb.Key as URL-safe base64-encoded string."""
  return obj.urlsafe()


def encode_future(obj):
  """Encode an ndb.Future instance."""
  return obj.get_result()


def encode_datetime(obj):
  """Encode a datetime.datetime or datetime.date object as an ISO 8601 format string."""
  # Reformat the date slightly for better JS compatibility.
  # Offset-naive dates need 'Z' appended for JS.
  # datetime.date objects don't have or need tzinfo, so don't append 'Z'.
  zone = '' if getattr(obj, 'tzinfo', True) else 'Z'
  return obj.isoformat() + zone


def encode_complex(obj):
  """Convert a complex number object into a list containing the real and imaginary values."""
  return [obj.real, obj.imag]


def encode_basevalue(obj):
  """Retrieve the actual value from a ndb.model._BaseValue.

  This is a convenience function to assist with the following issue:
  https://code.google.com/p/appengine-ndb-experiment/issues/detail?id=208
  """
  return obj.b_val


NDB_TYPE_ENCODING = {
  ndb.MetaModel: encode_model,
  ndb.Query: encode_generator,
  ndb.QueryIterator: encode_generator,
  ndb.Key: encode_key_as_entity,
  ndb.Future: encode_future,
  datetime.date: encode_datetime,
  datetime.datetime: encode_datetime,
  time.struct_time: encode_generator,
  types.ComplexType: encode_complex,
  ndb.model._BaseValue: encode_basevalue,
}

# Sort the types so any iteration is in a deterministic order
NDB_TYPES = (
  ndb.Future,
  ndb.Key,
  ndb.MetaModel,
  ndb.Query,
  ndb.QueryIterator,
  ndb.model._BaseValue,
  types.ComplexType,
  datetime.date,
  datetime.datetime,
  time.struct_time,
)


def _object_hook_handler(val):
  """Handles decoding of nested date strings."""
  return {k: _decode_date(v) for k, v in val.iteritems()}


def _decode_date(val):
  """Tries to decode strings that look like dates into datetime objects."""
  if isinstance(val, basestring) and DATE_RE.match(val):
    try:
      dt = arrow.parser.DateTimeParser().parse_iso(val)
      # Check for UTC.
      if val.endswith(('+00:00', '-00:00', 'Z')):
        # Then remove tzinfo for gae, which is offset-naive.
        dt = dt.replace(tzinfo=None)
      return dt
    except (TypeError, ValueError):
      pass
  return val


class NdbDecoder(json.JSONDecoder):
  """Extend the JSON decoder to add support for datetime objects."""

  def __init__(self, **kwargs):
    """Override the default __init__ in order to specify our own parameters."""
    json.JSONDecoder.__init__(self, object_hook=_object_hook_handler, **kwargs)

  def decode(self, val):
    """Override of the default decode method that also uses decode_date."""
    # First try the date decoder.
    new_val = _decode_date(val)
    if val != new_val:
      return new_val
    # Fall back to the default decoder.
    return json.JSONDecoder.decode(self, val)


class NdbEncoder(json.JSONEncoder):
  """Extend the JSON encoder to add support for NDB Models."""

  def __init__(self, **kwargs):
    self._ndb_type_encoding = NDB_TYPE_ENCODING.copy()
    self._cached_type_encoding = {}

    keys_as_entities = kwargs.pop('ndb_keys_as_entities', False)
    keys_as_pairs = kwargs.pop('ndb_keys_as_pairs', False)
    keys_as_urlsafe = kwargs.pop('ndb_keys_as_urlsafe', False)

    if any((keys_as_entities, keys_as_pairs, keys_as_urlsafe)):
      # Validate that only one of three flags is True
      if ((keys_as_entities and keys_as_pairs)
          or (keys_as_entities and keys_as_urlsafe)
          or (keys_as_pairs and keys_as_urlsafe)):
        raise ValueError('Only one of arguments ndb_keys_as_entities, ndb_keys_as_pairs, ndb_keys_as_urlsafe can be True')

      if keys_as_pairs:
        self._ndb_type_encoding[ndb.Key] = encode_key_as_pair
      elif keys_as_urlsafe:
        self._ndb_type_encoding[ndb.Key] = encode_key_as_urlsafe
      else:
        self._ndb_type_encoding[ndb.Key] = encode_key_as_entity

    json.JSONEncoder.__init__(self, **kwargs)

  def default(self, obj):
    """Overriding the default JSONEncoder.default for NDB support."""
    obj_type = type(obj)
    fn = self._ndb_type_encoding.get(obj_type) or self._cached_type_encoding.get(obj_type) or self._ndb_type_encoding.get(getattr(obj, '__metaclass__', None))
    if fn:
      return fn(obj)

    # Try to encode subclasses of types
    for ndb_type in NDB_TYPES:
      if isinstance(obj, ndb_type):
        obj_type = ndb_type
        break

    fn = self._ndb_type_encoding.get(obj_type)
    if fn:
      self._cached_type_encoding[getattr(obj, '__metaclass__', type(obj))] = fn
      return fn(obj)

    return json.JSONEncoder.default(self, obj)


def dumps(ndb_model, **kwargs):
  """Custom json dumps using the custom encoder above."""
  return NdbEncoder(**kwargs).encode(ndb_model)


def dump(ndb_model, fp, **kwargs):
  """Custom json dump using the custom encoder above."""
  for chunk in NdbEncoder(**kwargs).iterencode(ndb_model):
    fp.write(chunk)


def loads(json_str, **kwargs):
  """Custom json loads function that converts datetime strings."""
  return NdbDecoder(**kwargs).decode(json_str)
