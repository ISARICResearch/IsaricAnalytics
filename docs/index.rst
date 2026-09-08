================
ISARIC Analytics
================

The `ISARIC Analytics <https://github.com/ISARICResearch/IsaricAnalytics/>`_ library (:code:`isaricanalytics`) is for users requiring or interested in:

- Raw data extraction and cleaning from `REDCap <https://projectredcap.org>`_ project databases.
- Transforming custom raw clinical datasets into the `ISARIC data schema <https://isaric-arc.readthedocs.io/en/latest/sources/isaric-data-schema.html>`_.
- Data analytics & visualisation with `Pandas <pandas.pydata.org>`_ and `Plotly <plotly.com/python>`_.

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

The documentation is currently limited to an :ref:`API reference <api-reference>` for all the core public libraries. Further documentation on using the core libraries, including a plot gallery showing a range of plots and figures that can be generated using the visualisation library, will be added over time.

If you're interested in contributing please look at the :ref:`contributing guide <contributing-guide>`.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/api-reference
   sources/contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
