Bullseye
=======

Version 0.1.0

Bullseye is a free/libre program that allows you to perform various actions with
the messaging service `Discord`_. Currently, it allows you to:

* Create an account
* Verify your email address
* View your account tag
* Change your username, email address, password, and avatar
* Change safety and privacy settings
* List servers you’re in and members in those servers
* Transfer and delete servers you own
* Accept server invites
* Delete your account

Actions that require you to complete a CAPTCHA (often required when logging in
from a new location, for example) are supported by using `librecaptcha`_.

For free/libre software that allows you to send and receive messages with
Discord, check out `purple-discord`_.

.. _Discord: https://en.wikipedia.org/wiki/Discord_(software)
.. _librecaptcha: https://github.com/taylordotfish/librecaptcha
.. _purple-discord: https://github.com/EionRobb/purple-discord


Installation
------------

From PyPI
~~~~~~~~~

Install with `pip`_::

    sudo pip3 install Bullseye-discord

To install locally, run without ``sudo`` and add the ``--user`` option.


From the Git repository
~~~~~~~~~~~~~~~~~~~~~~~

Clone the repository with the following commands (you’ll need to have `Git`_
installed)::

    git clone https://github.com/taylordotfish/Bullseye
    cd Bullseye

Then install with `pip`_::

    sudo pip3 install .

To install locally, run without ``sudo`` and add the ``--user`` option.


Run without installing
~~~~~~~~~~~~~~~~~~~~~~

Run the first set of commands in the previous section to clone the repository.
Then, install the required dependencies by running::

    sudo ./deps/install-dependencies.py

To install the dependencies locally, run without ``sudo`` and add ``--user``.

.. _pip: https://pip.pypa.io
.. _Git: https://git-scm.com


Usage
-----

If you installed Bullseye, simply run ``Bullseye``, or see ``Bullseye -h`` for
more options. If you didn’t install it, use ``./Bullseye.py`` instead of
``Bullseye``.

If an action requires you to solve a CAPTCHA, Bullseye will use
`librecaptcha`_’s GTK 3 GUI, if available, unless the environment variable
``LIBRECAPTCHA_NO_GUI`` is set to a non-empty string.

.. _librecaptcha: https://github.com/taylordotfish/librecaptcha


Dependencies
------------

* `Python`_ ≥ 3.5
* The following Python packages:

  - `Pillow`_
  - `requests`_
  - `librecaptcha[gtk] <librecaptcha-pkg_>`_
  - `keyring`_

The installation instructions above handle installing the Python packages.
Alternatively, running ``pip3 install -r deps/requirements.lock`` will install
specific versions of the dependencies that have been tested (but may be
outdated or have problems).

.. _Python: https://www.python.org/
.. _Pillow: https://pypi.org/project/Pillow/
.. _requests: https://pypi.org/project/requests/
.. _librecaptcha-pkg: https://pypi.org/project/librecaptcha/
.. _keyring: https://pypi.org/project/keyring/
