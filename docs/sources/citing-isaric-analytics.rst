.. _citing-isaric-analytics:

Citing ISARICAnalytics
======================

ISARICAnalytics is **published** on `GitHub <https://github.com/ISARICResearch/ISARICAnalytics/releases>`_. It currently does not have a DOI, although this is planned.

ISARICAnalytics can be **cited** as follows:

	Edinburgh T, Garcia-Gallo E, Peres I, Gusberti T, Raffaini L, Murthy SR, Wilson AD. IsaricAnalytics (v0.3.0). *ISARIC* 2026. https://github.com/ISARICResearch/IsaricAnalytics

.. _note-for-maintainers-and-contributors:

A Note For Maintainers & Contributors
-------------------------------------

Maintainers and contributors should note that the `citation file <https://github.com/ISARICResearch/ISARICAnalytics/blob/main/CITATION.cff>`_ should be kept up-to-date with changes in authorship. The file can be validated on the command line using the `cffconvert <https://github.com/citation-file-format/cffconvert>`_ library using the following command run from the root of the ARC repository:

.. code:: shell

   cffconvert --validate

Any reported errors should be fixed, and the file staged and committed in the normal way. Citation file validation is included in the pre-commit status checks that happen automatically in GitHub on branch and PR updates.
