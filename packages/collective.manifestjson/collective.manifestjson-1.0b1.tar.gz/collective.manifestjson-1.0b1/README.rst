.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.manifestjson/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.manifestjson/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.manifestjson/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.manifestjson?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.manifestjson/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.manifestjson

.. image:: https://img.shields.io/pypi/v/collective.manifestjson.svg
    :target: https://pypi.python.org/pypi/collective.manifestjson/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.manifestjson.svg
    :target: https://pypi.python.org/pypi/collective.manifestjson
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.manifestjson.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.manifestjson.svg
    :target: https://pypi.python.org/pypi/collective.manifestjson/
    :alt: License


=======================
collective.manifestjson
=======================

Allows to add manifest configuration in control panel and provides a view to render it as manifest.json

Features
--------

- provides a control panel where one can configure the content of a manifest.json file
- allows enabling/disabling the manifest.json in HTML header



Usage
-----

- Install and enable the addon
- Configure your manifest in the Manifest settings control panel
- Make sure you have the referenced image folder and icons added and published, be default `/images/icons`
- Open the website with you smartphone and select `Add to Home Screen` (Chrome) or `Install` (Firefox) and place the website as an app on your home screen.


Translations
------------

This product has been translated into

- German (Maik Derstappen - MrTango)


Installation
------------

Install collective.manifestjson by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.manifestjson


and then running ``bin/buildout``


Authors
-------

This add-on was build by `Derico <https://derico.de>`_ [MrTango].


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.manifestjson/issues
- Source Code: https://github.com/collective/collective.manifestjson


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
