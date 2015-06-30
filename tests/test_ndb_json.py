#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ndb_json
----------------------------------

Tests for `gaek` module.
"""

import datetime
import json
import unittest
import cStringIO

from gaek import ndb_json


class TestNdbJson(unittest.TestCase):

    def setUp(self):
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


if __name__ == '__main__':
    unittest.main()
