====================
django-shop-netaxept
====================

A payment module for django-shop using Netaxept

Installation
------------

For the development version:

::

    pip install -e git+git://github.com/fivethreeo/django-shop-netaxept.git#egg=django-shop-netaxept

Configuration
-------------

Add ``djnetaxept`` and ``shop_netaxept`` to ``settings.INSTALLED_APPS`` and run:

::

    manage.py syncdb

