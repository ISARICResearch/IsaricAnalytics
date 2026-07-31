# IsaricAnalytics

[![CodeQL](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/github-code-scanning/codeql)
[![pre-commit](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/pre-commit.yml)
[![Tests (python versions)](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/test.yml/badge.svg)](https://github.com/ISARICResearch/IsaricAnalytics/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/ISARICResearch/IsaricAnalytics/graph/badge.svg?token=Q0A84OK6E5)](https://codecov.io/gh/ISARICResearch/IsaricAnalytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

IsaricAnalytics is a data analysis toolkit to support fast analysis of clinical data during emerging infectious disease outbreaks. It supports medical statistics and traditional machine learning, with analysis pipelines that follow methodological best practices.

IsaricAnalytics assumes a flexible [data schema](https://github.com/IsaricResearch/IsaricAnalytics/schema) based on ISARIC's tools for data collection, [ARC](https://github.com/IsaricResarch/ARC) and [BRIDGE](https://github.com/IsaricResarch/BRIDGE), but is general enough for other data sources if the data is transformed to the same structure.

ISARIC encourages data collection using standardised variable names, definitions, answer options, codelists, and more. In addition, the purpose of data collected using ISARIC tools is for clinical characterisation during outbreaks. This means that the data share characteristics that allow some automation during research analyses and the re-use of elements of analysis pipelines to similar contexts. This package is designed to support Reusable Analytical Pipelines for Infectious Diseases (RAPIDs), which is based on the concept of [Reproducible Analytical Pipelines](https://analysisfunction.civilservice.gov.uk/support/reproducible-analytical-pipelines/).

## Contributors

If you're interested in contributing please consult the [contributing guide](https://github.com/ISARICResearch/IsaricAnalytics/blob/main/CONTRIBUTING.md). This applies to documentation contributions also.

All contributors are listed below:

* Tom Edinburgh - tom.edinburgh@ndm.ox.ac.uk
* Sandeep Murthy - sandeep.murthy@ndm.ox.ac.uk
* Alasdair Wilson - alasdair.wilson@rse.ox.ac.uk

## Maintainers

Repository members with administrative privileges who manage access, maintenance and version control issues are listed below:

* Esteban Garcia-Gallo - esteban.garcia@ndm.ox.ac.uk
* Sandeep Murthy - sandeep.murthy@ndm.ox.ac.uk
* Alasdair Wilson - alasdair.wilson@rse.ox.ac.uk

## Documentation

Project documentation is available at https://isaricanalytics.readthedocs.io/en/latest. It is built with [Sphinx](https://www.sphinx-doc.org/en/) from content and configuration defined in the [`docs`](https://github.com/ISARICResearch/VERTEX/tree/main/docs) subfolder.

The documentation is maintained and updated together with the codebase, and some sections may be incomplete at any given point - contributions to documentation are also welcome and contributors can refer to the [contributions guide](https://github.com/ISARICResearch/IsaricAnalytics/blob/main/CONTRIBUTING.md).
