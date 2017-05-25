.. _quickstart:

Quickstart
==========

Eager to get started? This page gives a good introduction to Travian Legends API. It assumes you already have API module installed. If you do not, head over to the Installation section.

A Minimal Application
---------------------

A minimal application which use this API looks something like this:

.. code-block:: python
    :linenos:

    from travianapi import Account

    url = 'your server url'
    name = 'your username'
    password = 'your password'

    account = Account(url, name, password)

    # use account

