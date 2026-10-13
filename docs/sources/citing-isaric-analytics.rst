.. _citing-isaric-analytics:

Citing ISARICAnalytics
======================

ISARICAnalytics is **published** on `GitHub <https://github.com/ISARICResearch/ISARICAnalytics/releases>`_ and `Zenodo <https://zenodo.org/records/23340915>`_. It has the DOI:

`10.5281/zenodo.23340915 <https://doi.org/10.5281/zenodo.23340915>`_

ISARICAnalytics can be **cited** as follows:

	Edinburgh T, Garcia-Gallo E, Peres I, Gusberti T, Raffaini L, Murthy SR, Wilson AD. IsaricAnalytics (v0.3.0). *ISARIC* 2026. https://github.com/ISARICResearch/IsaricAnalytics

.. _note-for-maintainers-and-contributors:

A Note For Maintainers & Contributors
-------------------------------------

Maintainers and contributors should note that the `citation file <https://github.com/ISARICResearch/ISARICAnalytics/blob/main/CITATION.cff>`_ should be kept up-to-date with changes in authorship. The file can be validated on the command line using the `cffconvert <https://github.com/citation-file-format/cffconvert>`_ library using the following command run from the root of the ARC repository:

.. code:: shell

   cffconvert --validate

You should see validation succeeding:

.. code:: shell

   Citation metadata are valid according to schema version 1.2.0.

Any reported errors should be fixed, and the file staged and committed in the normal way. Citation file validation is included in the pre-commit status checks that happen automatically in GitHub on branch and PR updates.
