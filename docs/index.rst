================
ISARIC Analytics
================

The `ISARIC Analytics <https://github.com/ISARICResearch/IsaricAnalytics/>`_ library (:code:`isaricanalytics`) is for users requiring or interested in:

- REDCap data extraction
- ISARIC data analytics
- ISARIC data visualisation

ISARICAnalytics is licensed under the open source compliant `MIT license <https://opensource.org/license/mit>`_.

.. image:: _static/osi-badge-light.svg
   :target: https://opensource.org/license/mit
   :height: 200px
   :width:  200px

Installation
------------

Install with :program:`pip` directly from GitHub using:

.. code:: shell

   pip install -U git+https://github.com/ISARICResearch/ISARICAnalytics

This will install the default ``main`` branch of the repo, including all package dependencies (and sub-dependencies) - if you want a specific branch, tag or commit SHA use

.. code:: shell

   pip install -U git+https://github.com/ISARICResearch/ISARICAnalytics@<branch name or tag or commit SHA>

The minimum required Python version is 3.11.

Citation
--------

ISARICAnalytics can be cited as follows:

  Edinburgh T, Garcia-Gallo E, Peres I, Gusberti T, Raffaini L, Murthy SR, Wilson AD. IsaricAnalytics (v0.2.0). *ISARIC* 2026. https://github.com/ISARICResearch/IsaricAnalytics

All contributors listed in the citation file should be included.

Documentation
-------------

The documentation is currently limited to an API reference for all the core public libraries, but user tutorials, a visualisation gallery and additional documentation will be added in the future.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/api-reference
   sources/redcap-data
   sources/analytics
   sources/visualisation
   sources/contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
