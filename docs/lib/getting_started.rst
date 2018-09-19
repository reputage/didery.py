Getting Started
===============

You will need python 3.6 and libsodium installed to run didery.py. You
can find python 3.6 `here <https://www.python.org/downloads/>`__ and
libsodium `here <https://download.libsodium.org/doc/installation/>`__.

Installation
------------

To install didery.py start your virtual environment and run the command
below:

::

    $ pip install -e didery.py/

Importing
---------

.. code:: python

    import diderypy.lib as lib

    vk, sk, = lib.generating.keyGen()

    print(vk)
    print(sk)
