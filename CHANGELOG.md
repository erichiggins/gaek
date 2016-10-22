0.3.0
=====
- Added support for encoding `ndb.Key` objects as entities, pairs, or urlsafe-strings.
- Fixed a compatibility issue between `ndb_json` and `freezegun`.
- Fixed an issue where `'null'` could not be decoded properly.
- Fixed an issue where nested date strings were not decoded into `datetime` objects.

0.2.3
=====
- Fixed a bug in `environ.is_default_version()`
- Cleaned up `requirements.txt`

0.2.2
=====
- Build and file clean-ups.
- Configure Travis CI to auto-deploy to PyPi.


0.2.1
=====
- Patch version in order to replace uploaded sdist files on PyPi.


0.2.0
====
- Added the `environ` module.


0.1.2
=====
- Actually fix the MANIFEST.in contents.


0.1.1
=====
- Fixed issue in `MANIFEST.in` which excluded the `requirements.txt` files.


0.1.0
=====
- Initial release
- Added unit tests
- Support for `ndb_json.dump`, `ndb_json.dumps`, and `ndb_json.loads`
