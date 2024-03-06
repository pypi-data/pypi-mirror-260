past-time
=========

A simple tool to visualize the progress of the year based on the past days.

Installation
------------

The tool is available from the `Python Package Index <https://pypi.python
.org/pypi>`_.

.. code:: bash

    $ pip3 install past-time

Installation on Fedora and CentOS/RHEL with EPEL.

.. code:: bash

    $ dnf -y install past-time

For Nix or NixOS users is a package available. Keep in mind that the lastest releases might only
be present in the ``unstable`` channel.

.. code:: bash

   $ nix-env -iA nixos.past-time

Usage
-----

Execute the command to get a visual representation of the year's progress.

.. code:: bash

    $ past-time now

Development
-----------

For development is recommended to use a ``venv``.

.. code:: bash

    $ python3.6 -m venv .
    $ source bin/activate
    $ python3 setup.py develop

License
-------

``past-time`` is licensed under MIT, for more details check LICENSE.
