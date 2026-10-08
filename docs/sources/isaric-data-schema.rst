.. _isaric-data-schema:

==================
ISARIC Data Schema
==================

This is a brief guide to the :py:mod:`isaricanalytics.isaric_data_schema` library, which supports direct transformations of raw, custom clinical datasets into the standardised :doc:`ISARIC data schema <isaric-arc:sources/isaric-data-schema>` format, which can be analysed and visualised without much effort.

Before proceeding further, it is recommended to consult the ARC :doc:`ISARIC data schema guide <isaric-arc:sources/isaric-data-schema>` for more information on the core table (one-row-per-patient) and long table (multiple-rows-per-patient) output formats, and the required columns within each table, and also the ARC :doc:`parser guide <isaric-arc:sources/writing-a-parser>` on how to write the parser file.

.. _schema-transformation-pipeline:

The Schema Transformation Pipeline
----------------------------------

The transformation pipeline is implemented as a single function :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema`, which can produce either the basic ISARIC data schema outputs, or a VERTEX-style outputs, as described below.

.. _schema-transformation-basic:

Basic Schema Outputs
~~~~~~~~~~~~~~~~~~~~

To produce the basic ISARIC data schema outputs call the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function with three required arguments:

* ``parser_file`` - the (relative or absolute) file path of the :file:`.toml` **parser file** that describes how columns in the source dataset map to columns in the core or long table versions of the ISARIC data schema. If both core and long table outputs are required the parser file will need to define both sets of mappings.

* ``data_file`` - the (relative or absolute) file path of the **data file** containing the raw data.

* ``arc_version`` - the **ARC release version/tag**, which can also be obtained from the new :doc:`ARC Python package <isaric-arc:sources/arc-python>` using the :py:func:`isaric-arc:arc.arc_core.get_arc_versions` function.

Provided you have cloned the `ARC repository <https://github.com/ISARICResearch/ARC>`_ side-by-side with your project, then the following snippet shows the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function at work:

.. code:: python

   >>> tables = transform_to_isaric_data_schema('../ARC/docs/examples/example_parser.toml', '../ARC/docs/examples/example_data.csv', 'v1.6.1')
   [covid-study] parsing example_data.csv: 100%|███████████████████████████████████████████| 5/5 [00:00<00:00, 51.04it/s]
   [covid-study] validating core table: 5it [00:00, 52038.51it/s]
   [covid-study] validating long table: 109it [00:00, 128819.14it/s]
   2026-10-06 16:36:32 [INFO] arc.arc_core: version: v1.6.1

   >>> tables['core']
     subjid       siteid  ... adtl_valid                                         adtl_error
   0   C001  SITE-GBR-01  ...       True                                                NaN
   1   C002  SITE-DEU-01  ...       True                                                NaN
   2   C003  SITE-USA-01  ...       True                                                NaN
   3   C004  SITE-GBR-02  ...      False  data must contain ['subjid', 'siteid', 'datase...
   4   C005  SITE-ESP-01  ...       True                                                NaN

   [5 rows x 13 columns]

   >>> tables['long']
              date   dataset_id attribute_status subjid  ... adtl_valid attribute_unit value_num duration
   0    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   1    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   2    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   3    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   4    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   ..          ...          ...              ...    ...  ...        ...            ...       ...      ...
   104  2023-01-21  COVID-STUDY              VAL   C005  ...       True         10^9/L       9.2      NaN
   105  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   106         NaN  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   107  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   108  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN

   [109 rows x 12 columns]

The core table contians individual patient records, that is, with each row representing a distinct patient record, while the long table contains multiple records per patient, with each record representing an observation about a patient.

.. _schema-transformation-vertex-outputs:

VERTEX-style Outputs
~~~~~~~~~~~~~~~~~~~~

If you're a `VERTEX <https://vertex.isaric.org>`_ user, and interested in writing insight panels for a VERTEX dashboard then with the additional optional argument of ``as_vertex_data=True`` the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function will return a dictionary of the main VERTEX dashboard input file dataframes (``df_map``, ``daily``, and ``dictiomary``) as shown in the snippet below, that can be used to set up a compatible :doc:`VERTEX project <isaric-vertex:sources/app#project-structure>`.

.. code:: python

   >>> vertex_project_data = transform_to_isaric_data_schema('../ARC/docs/examples/example_parser.toml', '../ARC/docs/examples/example_data.csv', 'v1.6.1', as_vertex_data=True)
   [covid-study] parsing example_data.csv: 100%|██████████████████████████████████████████| 5/5 [00:00<00:00, 530.95it/s]
   [covid-study] validating core table: 5it [00:00, 36986.81it/s]
   [covid-study] validating long table: 109it [00:00, 180774.67it/s]
   >>>
   >>> vertex_project_data.keys()
   dict_keys(['df_map', 'daily', 'dictionary'])
   >>>
   >>> vertex_project_data['df_map']
     subjid       siteid  ... adtl_valid                                         adtl_error
   0   C001  SITE-GBR-01  ...       True                                                NaN
   1   C002  SITE-DEU-01  ...       True                                                NaN
   2   C003  SITE-USA-01  ...       True                                                NaN
   3   C004  SITE-GBR-02  ...      False  data must contain ['subjid', 'siteid', 'datase...
   4   C005  SITE-ESP-01  ...       True                                                NaN

   [5 rows x 13 columns]
   >>>
   >>> vertex_project_data['daily']
              date   dataset_id attribute_status subjid  ... adtl_valid attribute_unit value_num duration
   0    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   1    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   2    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   3    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   4    2023-01-10  COVID-STUDY              VAL   C001  ...       True            NaN       NaN      NaN
   ..          ...          ...              ...    ...  ...        ...            ...       ...      ...
   104  2023-01-21  COVID-STUDY              VAL   C005  ...       True         10^9/L       9.2      NaN
   105  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   106         NaN  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   107  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN
   108  2023-01-21  COVID-STUDY              VAL   C005  ...       True            NaN       NaN      NaN

   [109 rows x 12 columns]
   >>>
   >>> vertex_project_data['dictionary']
                 Form             Section  ... Branch                                   Question_english
   0     presentation                 NaN  ...                   Participant Identification Number (PIN)
   1     presentation  INCLUSION CRITERIA  ...         Suspected or confirmed infection, condition, o...
   2     presentation  INCLUSION CRITERIA  ...         Is the suspected or confirmed infection, condi...
   3     presentation  INCLUSION CRITERIA  ...                                Case classification status
   4     presentation  INCLUSION CRITERIA  ...                                        Reason for testing
   ...            ...                 ...  ...    ...                                                ...
   1752    withdrawal          WITHDRAWAL  ...                                        Date of withdrawal
   1753    withdrawal          WITHDRAWAL  ...                                     Reason for withdrawal
   1754    withdrawal          WITHDRAWAL  ...         Did the participant withdraw from active parti...
   1755    withdrawal          WITHDRAWAL  ...         Did the participant withdraw consent to use da...
   1756    withdrawal          WITHDRAWAL  ...         Did the participant withdraw consent to use sa...

   [1757 rows x 38 columns]

These VERTEX project data files should be exported to CSVs via the :py:meth:`pandas.DataFrame.to_csv` method (without the dataframe index, i.e. with ``index=False``) first in order to set up the VERTEX project.
