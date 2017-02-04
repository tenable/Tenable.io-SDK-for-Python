Tenable.io SDK for Python
=========================

Tenable.io SDK for Python

Configuration
~~~~~~~~~~~~~

Access key and secret key are needed to authenticate with the
`Tenable Cloud API <https://cloud.tenable.com/api>`_. There are three ways to
configure the ``TenableIOClient`` with the keys.

INI File
^^^^^^^^

| A ``tenable_io.ini`` can be created in the working directory. See
  ``tenable_io.ini.example`` on what it should look like.
| Note: The ``tenable_io.ini.example`` file is in Jinja template format.

``TenableIOClient`` Constructor Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    TenableIOClient(access_key='YOUR_ACCESS_KEY', secret_key='YOUR_SECRET_KEY')

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

TenableIOClient looks for the environment variables ``TENABLEIO_ACCESS_KEY``
and ``TENABLEIO_SECRET_KEY``.

Python Version
~~~~~~~~~~~~~~

2.7, 3.4

Development
~~~~~~~~~~~

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
~~~~~~~~~

.. code:: sh

    $ py.test

Documentations
~~~~~~~~~~~~~~

To generate/force update the RST documentations from docstrings.

.. code:: sh

    $ sphinx-apidoc -f -o doc/source tenable_io

Generate HTML documentation.

.. code:: sh

    $ cd doc
    $ make clean && make html
