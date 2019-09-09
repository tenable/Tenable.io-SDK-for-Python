Running SDK Tests
=========================
Configuring and running tests is only recommended if you intend to contribute new code or fixes to the SDK.

*Most* tests will run against pre-recorded API responses which are provided using the pytest-vcr library. These are useful for testing
modifications to existing API endpoints, but are insufficient if adding new endpoints or parameters. When adding new endpoints or modifying existing
endpoints it's recommended to run the tests using the ``--disable-vcr`` pytest argument, which completely disables vcr playback/recording.

Dependencies
------------
There are additional dependencies which must be installed to run tests. Namely:

pytest-vcr-1.0.2 or above
pytest-xdist-1.29.0 or above

You can install these by running
.. code:: sh

    $ pip install -r requirements-build.txt

Run Tests
------------
Additional configuration is needed for tests to correctly run. See the
``[tenable_io-test]`` section under ``tenable_io.ini.example``. Such
configuration can be done via the INI file ``tenable_io.ini`` or environment
variables.

.. code:: sh

    $ pytest -n=2

Notes for New Tests
--------------------
New tests are expected to pass reliably and have the ability to be run in parallel with other tests.

When testing it is recommended that you have a separate account to test with as the test can result in a messy environment.

If you are running tests without vcr enable the tests will expect some prerequisites in order to pass, such as >1 linked agents, >1 linked scanners, >1 existing assets, and >1 existing vulnerabilities.
