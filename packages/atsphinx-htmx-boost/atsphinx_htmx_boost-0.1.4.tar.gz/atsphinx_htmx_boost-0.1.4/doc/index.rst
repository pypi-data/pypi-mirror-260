====
Home
====

.. note:: This is experimental extension.

``atsphinx-htmx-boost`` is Sphinx-extension that will improve user-experience of documents by `HTMX <https://htmx.org>`_.

Getting started
===============

Installation
------------

This is published on PyPI. You can install by ``pip`` command.

.. code:: console

   pip install atsphinx-htmx-boost

If you use package manager, Add this into as dependencies.

.. code-block:: toml
   :caption: pyproject.toml
   :name: pyprojec.toml

   [project]
   dependencies = [
     "atsphinx-htmx-boost",
   ]

Usage
-----

This has extra options to work.
You can only register as extension into your ``conf.py``.

.. code-block:: python
   :caption: conf.py
   :name: conf.py

   extensions = [
       # Add it!
       "atsphinx.htmx_boost",
   ]

Contents
========

.. toctree::
   :maxdepth: 2
   :titlesonly:

   changelogs
