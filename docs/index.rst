================
ISARIC Analytics
================

The `ISARIC Analytics <https://github.com/ISARICResearch/IsaricAnalytics/>`_ library (:code:`isaricanalytics`) is for users requiring or interested in:

- REDCap data extraction
- Data analytics and/or visualisation

in the setting of clinical epidemiology.

ISARICAnalytics is licensed under the `MIT license <https://opensource.org/license/mit>`_.

.. image:: _static/osi-badge-light.svg
   :target: https://opensource.org/license/mit
   :height: 100px
   :width:  100px

Installation
------------

Install with :program:`pip` directly from GitHub using:

.. code:: shell

   pip install -U git+https://github.com/ISARICResearch/ISARICAnalytics

This will install the default ``main`` branch of the repo, including all package dependencies (and sub-dependencies) - if you want a specific branch, tag or commit SHA use

.. code:: shell

   pip install -U git+https://github.com/ISARICResearch/ISARICAnalytics@<branch name or tag or commit SHA>

The minimum required Python version is 3.11.

Documentation
-------------

The documentation is currently limited mainly to an :ref:`API reference <api-reference>` for all the core public libraries, a plot gallery for the :py:mod:`~isaricanalytics.visualisation` library, and a :ref:`contributing <contributing-guide>` guide. More content will be added over time.

See the linked pages below for more information on how to use the libraries or to contribute to their development. Some pages may still be under development.


.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/redcap-data
   sources/analytics
   sources/visualisation/index
   sources/citing-isaric-analytics
   sources/api-reference
   sources/contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
