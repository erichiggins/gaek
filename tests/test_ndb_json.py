# -*- coding: utf-8 -*-

"""
test_ndb_json
----------------------------------

Tests for `gaek` module.
"""

import datetime
import json
import mock
import unittest
import cStringIO

from google.appengine.ext import ndb
from nose import tools

from gaek import ndb_json


class TestNdbJson(unittest.TestCase):

    def setUp(self):
      self.ndb_mock = mock.Mock()
      self.ndb_mock.__metaclass__ = ndb.Key
      self.ndb_mock.urlsafe = mock.Mock(return_value='urlsafe')
      self.ndb_mock.pairs = mock.Mock(return_value='pairs')
      self.ndb_mock.get_async = mock.Mock(return_value='get_async')
      pass

    def tearDown(self):
        pass

    def test_dumps_with_ndb_values(self):
        """Assert functional with NDB datastore values."""
        pass

    def test_dumps_with_naive_values(self):
        """Assert functional parity with `json.dump` for naive values."""
        assert json.dumps({'bool true': True}) == ndb_json.dumps({'bool true': True})
        assert json.dumps({'bool false': False}) == ndb_json.dumps({'bool false': False})
        assert json.dumps({'empty str': ''}) == ndb_json.dumps({'empty str': ''})
        assert json.dumps({'str': 'hello world'}) == ndb_json.dumps({'str': 'hello world'})
        assert json.dumps({'unicode': u'(╯°□°)╯︵ ┻━┻'}) == ndb_json.dumps({'unicode': u'(╯°□°)╯︵ ┻━┻'})
        assert json.dumps({'int': 12345}) == ndb_json.dumps({'int': 12345})
        assert json.dumps({'float': 1.2345}) == ndb_json.dumps({'float': 1.2345})
        assert json.dumps({'str int': '12345'}) == ndb_json.dumps({'str int': '12345'})
        assert json.dumps({'str float': '1.2345'}) == ndb_json.dumps({'str float': '1.2345'})

    def test_dump_with_naive_values(self):
        """Assert functional parity with `json.dump`, for use with file-like objects."""
        json_fp = cStringIO.StringIO()
        ndb_json_fp = cStringIO.StringIO()

        payload = {
            'unicode': u'(╯°□°)╯︵ ┻━┻',
        }

        json.dump(payload, json_fp)
        ndb_json.dump(payload, ndb_json_fp)

        assert json_fp.getvalue() == ndb_json_fp.getvalue()
        json_fp.close()
        ndb_json_fp.close()

    def test_dumps_with_subclassed_type(self):
        """ Assert that a subclass of a supported type will encode as JSON properly """
        class MyDateTime(datetime.datetime):
            pass

        subclass_parsed = ndb_json.dumps({'a datetime': MyDateTime(2015, 10, 1)})
        original_parsed = ndb_json.dumps({'a datetime': datetime.datetime(2015, 10, 1)})
        assert subclass_parsed == original_parsed

    def test_loads_with_naive_values(self):
        payload_str = json.dumps({
            'bool true': True,
            'bool false': False,
            'empty str': '',
            'str': 'hello world',
            'unicode': u'(╯°□°)╯︵ ┻━┻',
            'int': 12345,
            'float': 1.2345,
            'str int': '12345',
            'str float': '1.2345',
        })

        parsed = ndb_json.loads(payload_str)

        assert True == parsed['bool true']
        assert False == parsed['bool false']
        assert '' == parsed['empty str']
        assert 'hello world' == parsed['str']
        assert u'(╯°□°)╯︵ ┻━┻' == parsed['unicode']
        assert 12345 == parsed['int']
        assert 1.2345 == parsed['float']
        assert '12345' == parsed['str int']
        assert '1.2345' == parsed['str float']

    def test_loads_with_date_and_time_values(self):
        """Assert that date/time-like strings are parsed properly."""
        assert datetime.datetime(2015, 1, 1) == ndb_json.loads(datetime.date(2015, 1, 1).isoformat())

        payload_str = json.dumps({
            'date': datetime.date(2015, 1, 1).isoformat(),
            'datetime': datetime.datetime(2015, 1, 1, 12, 0, 0, 0).isoformat(),
            'time': '12:30',
            'non-date': '12-15',
            'double-hyphen non-date': '12-15-0',
        })

        parsed = ndb_json.loads(payload_str)

        # TODO(erichiggins): It may be better for dates to be parsed as instances of `datetime.date`.
        assert datetime.datetime(2015, 1, 1) == parsed['date']
        assert datetime.datetime(2015, 1, 1, 12, 0, 0, 0) == parsed['datetime']
        assert '12:30' == parsed['time']
        assert '12-15' == parsed['non-date']
        assert '12-15-0' == parsed['double-hyphen non-date']

    def test_loads_with_nested_datetime(self):
        """Assert the object hooks work as intended."""
        payload_str = json.dumps({
          'nested': {'datetime': datetime.datetime(2016, 1, 1, 12).isoformat()},
        })
        parsed = ndb_json.loads(payload_str)
        assert datetime.datetime(2016, 1, 1, 12, 0, 0, 0) == parsed['nested']['datetime']

    def test_invalid_arguments(self):
      self.assertRaises(ValueError,
                        ndb_json.NdbEncoder,
                        ndb_keys_as_entities=True,
                        ndb_keys_as_pairs=True,
                        ndb_keys_as_urlsafe=True)
      self.assertRaises(ValueError,
                        ndb_json.NdbEncoder,
                        ndb_keys_as_entities=False,
                        ndb_keys_as_pairs=True,
                        ndb_keys_as_urlsafe=True)
      self.assertRaises(ValueError,
                        ndb_json.NdbEncoder,
                        ndb_keys_as_entities=True,
                        ndb_keys_as_pairs=False,
                        ndb_keys_as_urlsafe=True)
      self.assertRaises(ValueError,
                        ndb_json.NdbEncoder,
                        ndb_keys_as_entities=True,
                        ndb_keys_as_pairs=True,
                        ndb_keys_as_urlsafe=False)

    def test_encode_key(self):
      some_obj = mock.Mock()
      ndb_json.encode_key(some_obj)
      self.assertEqual(1, some_obj.get_async.call_count)

    def test_encode_key_as_entity(self):
      some_obj = mock.Mock()
      ndb_json.encode_key_as_entity(some_obj)
      self.assertEqual(1, some_obj.get_async.call_count)

    def test_encode_key_as_pair(self):
      some_obj = mock.Mock()
      ndb_json.encode_key_as_pair(some_obj)
      self.assertEqual(1, some_obj.pairs.call_count)

    def test_encode_key_as_urlsafe(self):
      some_obj = mock.Mock()
      ndb_json.encode_key_as_urlsafe(some_obj)
      self.assertEqual(1, some_obj.urlsafe.call_count)

    def test_dumps__no_option_specified(self):
      obj = {
        "number": 1,
        "string": "is here",
        "key": self.ndb_mock
      }

      dump = ndb_json.dumps(obj, sort_keys=True)
      self.assertEqual('{"key": "get_async", "number": 1, "string": "is here"}', dump)

    def test_dumps__ndb_keys_as_entities(self):

      obj = {
        "number": 1,
        "string": "is here",
        "key": self.ndb_mock
      }

      dump = ndb_json.dumps(obj, sort_keys=True, ndb_keys_as_entities=True)
      self.assertEqual('{"key": "get_async", "number": 1, "string": "is here"}', dump)

    def test_dumps__ndb_keys_as_pairs(self):

      obj = {
        "number": 1,
        "string": "is here",
        "key": self.ndb_mock
      }

      dump = ndb_json.dumps(obj, sort_keys=True, ndb_keys_as_pairs=True)
      self.assertEqual('{"key": "pairs", "number": 1, "string": "is here"}', dump)

    def test_dumps__ndb_keys_as_urlsafe(self):

      obj = {
        "number": 1,
        "string": "is here",
        "key": self.ndb_mock
      }

      dump = ndb_json.dumps(obj, sort_keys=True, ndb_keys_as_urlsafe=True)
      self.assertEqual('{"key": "urlsafe", "number": 1, "string": "is here"}', dump)

    def test_loads_with_primitive_values(self):
        """Assert that primitive values are parsed properly."""
        test_cases = ['null', '2', 'Infinity', '1.2345']
        for s in test_cases:
            tools.eq_(json.loads(s), ndb_json.loads(s))

    def test_loads_with_other_collections(self):
        """Assert that array/list values are parsed properly."""
        test_cases = ['[1,2,3,4]', '[[0]]', '[[[{}]]]']
        for s in test_cases:
            tools.eq_(json.loads(s), ndb_json.loads(s))


if __name__ == '__main__':
    unittest.main()
