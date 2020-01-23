NOTICE: Tenable.io SDK for Python is being deprecated in favor of `pyTenable <https://github.com/tenable/pyTenable>`_
=====================================================================================================================

Tenable has decided to deprecate the ``tenable_io`` package in favor of the more widely used library,
`pyTenable <https://github.com/tenable/pyTenable>`_. `pyTenable <https://github.com/tenable/pyTenable>`_ offers all of
the same functionality as this package, as well as support for `tenable.sc <https://docs.tenable.com/Tenablesc.htm>`_.
However, it should be noted that ``pyTenable`` functions are not compatible with ``tenable_io`` functions.

Original README
===============
Tenable.io SDK for Python
=========================
.. image:: https://img.shields.io/pypi/v/tenable-io.svg?style=flat-square
    :target: https://pypi.python.org/pypi/tenable-io
.. image:: https://img.shields.io/github/license/tenable/Tenable.io-SDK-for-Python
   :target: https://github.com/tenable/Tenable.io-SDK-for-Python

Welcome to the Tenable.io SDK for Python. This library can be used to easily integrate with the `tenable.io <https://cloud.tenable.com/>`_ API.

For you coffee lovers, check out `Tenable.io SDK for Java <https://github.com/tenable/Tenable.io-SDK-for-Java>`_.

Report any issues `here <https://github.com/tenable/Tenable.io-SDK-for-Python/issues>`_.

Additional documentation is available in our `Developer Portal <https://developer.tenable.com/>`_.

Installation
------------

.. code-block:: bash

    $ pip install tenable_io

Quick Start
-----------

Quickest way to get started is to checkout the `example scripts <./examples/>`_.

Configuration
-------------

Access key and secret key are needed to authenticate with the
`Tenable Cloud API <https://cloud.tenable.com/api>`_. There are three ways to
supply the keys to the ``TenableIOClient``:

========== ==========
Precedence   Method
========== ==========
   1       Constructor Arguments
   2       INI File
   3       Environment Variables
========== ==========

TenableIOClient Constructor Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    TenableIOClient(access_key='YOUR_ACCESS_KEY', secret_key='YOUR_SECRET_KEY')

INI File
^^^^^^^^

| A ``tenable_io.ini`` can be created in the working directory. See
  ``tenable_io.ini.example`` on what it should look like.
| Note: The ``tenable_io.ini.example`` file is in Jinja template format.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

TenableIOClient looks for the environment variables ``TENABLEIO_ACCESS_KEY``
and ``TENABLEIO_SECRET_KEY``.

Python Version
--------------

2.7, 3.4+

Development
-----------

It is recommend to use ``virtualenv`` to setup an isolated local
environment.

.. code:: sh

    $ virtualenv .venv
    # To use a different python bin (i.e. python3).
    $ virtualenv .venv3 -p $(which python3)
    # To active the virtualenv
    $ source ./.venv/bin/activate

Install dependencies.

.. code:: sh

    $ pip install -r ./requirements.txt
    $ pip install -r ./requirements-build.txt

Run Tests
---------

Additional configuration is needed for tests to correctly run. See the
``[tenable_io-test]`` section under ``tenable_io.ini.example``. Such
configuration can be done via the INI file ``tenable_io.ini`` or environment
variables.

.. code:: sh

    $ py.test

Documentations
--------------

To generate/force update the RST documentations from docstrings.

.. code:: sh

    $ sphinx-apidoc -f -o doc/source tenable_io

Generate HTML documentation.

.. code:: sh

    $ cd doc
    $ make clean && make html
