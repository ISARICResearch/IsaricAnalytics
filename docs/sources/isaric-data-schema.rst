.. _isaric-data-schema:

==================
ISARIC Data Schema
==================

This is a brief guide to the :py:mod:`isaricanalytics.isaric_data_schema` library, which supports direct transformations of raw, custom clinical datasets into the standardised :doc:`ISARIC data schema <isaric-arc:sources/isaric-data-schema>` format, which can be analysed and visualised without much effort.

Before proceeding further, it is recommended to consult the ARC :doc:`ISARIC data schema guide <isaric-arc:sources/isaric-data-schema>` for more information on the core table (one-row-per-patient) and long table (multiple-rows-per-patient) output formats, and the required columns within each table, and also the ARC :doc:`parser guide <isaric-arc:sources/writing-a-parser>` on how to write the parser file.

.. _schema-transformation-pipeline:

The Schema Transformation Pipeline
----------------------------------

The main transformation pipeline, that converts a raw, custom clinical dataset and an associated parser to the ISARIC data schema format, is implemented by  :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema`. This function can produce either the basic ISARIC data schema outputs, or, optionally, VERTEX-style, analysis-ready outputs, as described below.

.. _schema-transformation-basic:

Basic Schema Outputs
~~~~~~~~~~~~~~~~~~~~

To produce the basic ISARIC data schema outputs call the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function with three required arguments:

* ``parser_file`` - the (relative or absolute) file path of the :file:`.toml` **parser file** that describes how columns in the source dataset map to columns in the core or long table versions of the ISARIC data schema. If both core and long table outputs are required the parser file will need to define both sets of mappings.

* ``data_file`` - the (relative or absolute) file path of the **data file** containing the raw data.

* ``arc_version`` - the **ARC release version/tag**, which can also be obtained from the new :doc:`ARC Python package <isaric-arc:sources/arc-python>` using the :py:func:`isaric-arc:arc.arc_core.get_arc_versions` function.

Provided you have cloned the `ARC repository <https://github.com/ISARICResearch/ARC>`_ side-by-side with your project, then the following snippet shows the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function at work, using a very simple `ARC example COVID-19 clinical dataset <https://github.com/ISARICResearch/ARC/tree/main/docs/examples>`_:

.. code:: python

   >>> import warnings; warnings.filterwarnings('ignore')
   >>> from isaricanalytics.isaric_data_schema import *
   >>> tables = transform_to_isaric_data_schema('../ARC/docs/examples/example_parser.toml', '../ARC/docs/examples/example_data.csv', 'v1.6.1')
  [covid-study] parsing example_data.csv: 100%|█████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 915.59it/s]
  [covid-study] validating core table: 5it [00:00, 46707.17it/s]
  [covid-study] validating long table: 109it [00:00, 191528.75it/s]
  2026-10-14 16:09:08 [INFO] arc.arc_core: version: v1.6.

   >>> tables['core']
   subjid       siteid   dataset_id  ...               outco_outcome adtl_valid                                         adtl_error
 0   C001  SITE-GBR-01  COVID-STUDY  ...            Discharged alive       True                                                NaN
 1   C002  SITE-DEU-01  COVID-STUDY  ...                       Death       True                                                NaN
 2   C003  SITE-USA-01  COVID-STUDY  ...            Discharged alive       True                                                NaN
 3   C004  SITE-GBR-02  COVID-STUDY  ...          Still hospitalised      False  data must contain ['subjid', 'siteid', 'datase...
 4   C005  SITE-ESP-01  COVID-STUDY  ...  Transfer to other facility       True                                                NaN

 [5 rows x 13 columns]

   >>> tables['long']
   subjid   dataset_id attribute_status         attribute arcver  ... value adtl_valid attribute_unit  value_num duration
 0     C001  COVID-STUDY              VAL    pres_symptpres  1.2.2  ...   Yes       True            NaN        NaN      NaN
 1     C001  COVID-STUDY              VAL       adsym_fever  1.2.2  ...   Yes       True            NaN        NaN      NaN
 2     C001  COVID-STUDY              VAL       adsym_cough  1.2.2  ...   Yes       True            NaN        NaN      NaN
 3     C001  COVID-STUDY              VAL  adsym_shortbreat  1.2.2  ...    No       True            NaN        NaN      NaN
 4     C001  COVID-STUDY              VAL     adsym_fatigue  1.2.2  ...   Yes       True            NaN        NaN      NaN
 ..     ...          ...              ...               ...    ...  ...   ...        ...            ...        ...      ...
 104   C005  COVID-STUDY              VAL     labs_wbccount  1.2.2  ...   NaN       True         10^9/L        9.2      NaN
 105   C005  COVID-STUDY              VAL    inter_suppleo2  1.2.2  ...    No       True            NaN        NaN      NaN
 106   C005  COVID-STUDY              VAL         crito_icu  1.2.2  ...    No       True            NaN        NaN      NaN
 107   C005  COVID-STUDY              VAL        compl_ards  1.2.2  ...    No       True            NaN        NaN      NaN
 108   C005  COVID-STUDY              VAL       compl_pneum  1.2.2  ...    No       True            NaN        NaN      NaN

 [109 rows x 12 columns]

The core table contains individual patient records, that is, with each row representing a distinct patient record, while the long table contains multiple records per patient, with each record representing an observation about a patient.

.. _schema-transformation-warnings:

Warnings
++++++++

If the raw dataset contains non-ARC columns or columns that are not mapped to any core or long table in the parser file warnings are displayed that include the mismatched column sets, as shown in the snippet below, with :py:mod:`warnings` turned on, as shown in the following snippet below:

.. code:: python

   >>> import warnings; warnings.filterwarnings('always')
   >>> tables = transform_to_isaric_data_schema('../ARC/docs/examples/example_parser.toml', '../ARC/docs/examples/example_data.csv', 'v1.6.1')
   [covid-study] parsing example_data.csv: 100%|█████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 915.59it/s]
   [covid-study] validating core table: 5it [00:00, 46707.17it/s]
   [covid-study] validating long table: 109it [00:00, 191528.75it/s]
   2026-10-14 16:09:08 [INFO] arc.arc_core: version: v1.6.1
   /Users/smurthy/Documents/srm/dev/ISARICAnalytics/src/isaricanalytics/isaric_data_schema.py:162: DeprecationWarning:

   The following core table columns are not in ARC v1.6.1: "adtl_error", "adtl_valid", "dataset_disease", "dataset_id", "demog_age_days", "demog_country_iso3", "siteid"

   Please check these columns.
   ...

   The following long table columns are not in ARC v1.6.1: "adtl_valid", "arcver", "attribute", "attribute_status", "attribute_unit", "dataset_id", "date", "duration", "phase", "value", "value_num"

   Please check these columns.
   ...

   The following source columns are not mapped to any core or long table columns: "ethnic", "icu_in", "icu_out", "icu_treat_antiviral_agents", "icu_treat_corticosteroids", "treat_antiviral_agents", "treat_corticosteroids"

   Please check these columns.
   ...
   >>>
   >>> tables['core']
     subjid       siteid   dataset_id  ...               outco_outcome adtl_valid                                         adtl_error
   0   C001  SITE-GBR-01  COVID-STUDY  ...            Discharged alive       True                                                NaN
   1   C002  SITE-DEU-01  COVID-STUDY  ...                       Death       True                                                NaN
   2   C003  SITE-USA-01  COVID-STUDY  ...            Discharged alive       True                                                NaN
   3   C004  SITE-GBR-02  COVID-STUDY  ...          Still hospitalised      False  data must contain ['subjid', 'siteid', 'datase...
   4   C005  SITE-ESP-01  COVID-STUDY  ...  Transfer to other facility       True                                                NaN

   [5 rows x 13 columns]
   >>>
   >>> tables['long']
     subjid   dataset_id attribute_status         attribute arcver  ... value adtl_valid attribute_unit  value_num duration
   0     C001  COVID-STUDY              VAL    pres_symptpres  1.2.2  ...   Yes       True            NaN        NaN      NaN
   1     C001  COVID-STUDY              VAL       adsym_fever  1.2.2  ...   Yes       True            NaN        NaN      NaN
   2     C001  COVID-STUDY              VAL       adsym_cough  1.2.2  ...   Yes       True            NaN        NaN      NaN
   3     C001  COVID-STUDY              VAL  adsym_shortbreat  1.2.2  ...    No       True            NaN        NaN      NaN
   4     C001  COVID-STUDY              VAL     adsym_fatigue  1.2.2  ...   Yes       True            NaN        NaN      NaN
   ..     ...          ...              ...               ...    ...  ...   ...        ...            ...        ...      ...
   104   C005  COVID-STUDY              VAL     labs_wbccount  1.2.2  ...   NaN       True         10^9/L        9.2      NaN
   105   C005  COVID-STUDY              VAL    inter_suppleo2  1.2.2  ...    No       True            NaN        NaN      NaN
   106   C005  COVID-STUDY              VAL         crito_icu  1.2.2  ...    No       True            NaN        NaN      NaN
   107   C005  COVID-STUDY              VAL        compl_ards  1.2.2  ...    No       True            NaN        NaN      NaN
   108   C005  COVID-STUDY              VAL       compl_pneum  1.2.2  ...    No       True            NaN        NaN      NaN

   [109 rows x 12 columns]

These should be addressed appropriately, which may include either removing some or all of the columns in question, or replacing them the equivalent ARC columns, and/or adding mappings in the parser file.

.. _schema-transformation-vertex-outputs:

VERTEX-style Outputs
~~~~~~~~~~~~~~~~~~~~

If you're a `VERTEX <https://vertex.isaric.org>`_ user, and interested in writing insight panels for a VERTEX dashboard, then you will need VERTEX-compatible dataframes representing one-row-per-patient data, as well as multi-row-per-patient observations data organised by patient interaction phase, and also the corresponding ARC data dictionary. This can be done in two ways depending on the format of the source data, as described below.

.. _vertex-outputs-from-raw-data:

From Raw Data
+++++++++++++

With the additional optional argument of ``as_vertex_data=True`` the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function will return a dictionary of dataframes required for VERTEX dashboard visualisation, as shown in the snippet below.

.. code:: python

   >>> import warnings; warnings.filterwarnings('ignore')
   >>> vertex_static_data = transform_to_isaric_data_schema('../ARC/docs/examples/example_parser.toml', '../ARC/docs/examples/example_data.csv', 'v1.6.1', as_vertex_data=True)
   [covid-study] parsing example_data.csv: 100%|███████████████████████████████████████████| 5/5 [00:00<00:00, 771.58it/s]
   [covid-study] validating core table: 5it [00:00, 45100.04it/s]
   [covid-study] validating long table: 109it [00:00, 217084.11it/s]
   2026-10-15 15:22:19 [INFO] arc.arc_core: version: v1.6.1
   INFO:arc.arc_core:version: v1.6.1
   >>> vertex_static_data.keys()
   dict_keys(['df_map', 'df_forms_dict', 'dictionary', 'quality_report'])

The transformation pipeline here works almost identically to non-VERTEX output option, except that there are additional steps to build the VERTEX-style output dataframes. The first and most important of these is named ``"df_map"``, which contains only one-row-per-patient data, organised by the ``subjid`` column, with list-valued observations data in all the other columns.

.. code:: python

   >>> vertex_static_data['df_map']
     subjid  ...                                          value_num
   0   C001  ...  [nan, nan, nan, nan, nan, nan, nan, nan, 38.1,...
   1   C002  ...  [nan, nan, nan, nan, nan, nan, nan, nan, 39.4,...
   2   C003  ...  [nan, nan, nan, nan, nan, nan, nan, nan, 37.8,...
   3   C004  ...  [nan, nan, nan, nan, nan, nan, nan, nan, 38.9,...
   4   C005  ...  [nan, nan, nan, nan, nan, nan, nan, nan, 37.6,...

  [5 rows x 20 columns]

There is also a ``"df_forms_dict"`` that is keyed by patient interaction phase, implemented via the unique values of the ``phase`` column:

.. code:: python

   >>> vertex_static_data['df_forms_dict'].keys()
   dict_keys([('during_observation',), ('outcome',), ('presentation',)])
   >>>
   >>> vertex_static_data['df_forms_dict']['presentation']
   subjid       siteid   dataset_id dataset_disease demog_country_iso3  ... arcver value value_num attribute_unit  duration
   0    C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2   Yes       NaN            NaN       NaN
   1    C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2   Yes       NaN            NaN       NaN
   2    C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2   Yes       NaN            NaN       NaN
   3    C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2    No       NaN            NaN       NaN
   4    C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2   Yes       NaN            NaN       NaN
   ..    ...          ...          ...             ...                ...  ...    ...   ...       ...            ...       ...
   64   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2   NaN      82.0            NaN       NaN
   65   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2   NaN      20.0            NaN       NaN
   66   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2   NaN      95.0            NaN       NaN
   67   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2   NaN     132.0            NaN       NaN
   68   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2   NaN      82.0            NaN       NaN

   [69 rows x 20 columns]
   >>>
   >>> vertex_static_data['df_forms_dict']['during_observation']
   subjid       siteid   dataset_id dataset_disease demog_country_iso3  ... arcver value value_num attribute_unit  duration
   0   C001  SITE-GBR-01  COVID-STUDY        COVID-19                GBR  ...  1.2.2    No       NaN            NaN       NaN
   1   C002  SITE-DEU-01  COVID-STUDY        COVID-19                DEU  ...  1.2.2   Yes       NaN            NaN      12.0
   2   C003  SITE-USA-01  COVID-STUDY        COVID-19                USA  ...  1.2.2    No       NaN            NaN       NaN
   3   C004  SITE-GBR-02  COVID-STUDY        COVID-19                GBR  ...  1.2.2    No       NaN            NaN       NaN
   4   C005  SITE-ESP-01  COVID-STUDY        COVID-19                ESP  ...  1.2.2    No       NaN            NaN       NaN

   [5 rows x 20 columns]
   >>>
   >>> vertex_static_data['df_forms_dict']['outcome']
   subjid       siteid   dataset_id dataset_disease  ...           value value_num attribute_unit duration
   0    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...             NaN      42.3           mg/L      NaN
   1    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...             NaN       1.2         10^9/L      NaN
   2    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...             NaN       7.8         10^9/L      NaN
   3    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   4    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   5    C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   6    C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             NaN     187.6           mg/L      NaN
   7    C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             NaN       0.4         10^9/L      NaN
   8    C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             NaN      12.3         10^9/L      NaN
   9    C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...  Corticosteroid       NaN            NaN      NaN
   10   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...       Antiviral       NaN            NaN      NaN
   11   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             Yes       NaN            NaN      NaN
   12   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             Yes       NaN            NaN      NaN
   13   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...             Yes       NaN            NaN      NaN
   14   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...       Bacterial       NaN            NaN      NaN
   15   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...             NaN      28.7           mg/L      NaN
   16   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...             NaN       0.9         10^9/L      NaN
   17   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...             NaN       8.1         10^9/L      NaN
   18   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...       Antiviral       NaN            NaN      NaN
   19   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...             Yes       NaN            NaN      NaN
   20   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   21   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   22   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...             NaN     134.2           mg/L      NaN
   23   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...             NaN       0.6         10^9/L      NaN
   24   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...             NaN      10.9         10^9/L      NaN
   25   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...  Corticosteroid       NaN            NaN      NaN
   26   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...             Yes       NaN            NaN      NaN
   27   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   28   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   29   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...             NaN      67.8           mg/L      NaN
   30   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...             NaN       1.1         10^9/L      NaN
   31   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...             NaN       9.2         10^9/L      NaN
   32   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   33   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN
   34   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...              No       NaN            NaN      NaN

   [35 rows x 20 columns]

The ARC data dictionary associated with the given ARC version is also returned via the ``"dictionary"`` key:

.. code:: python

   >>> vertex_static_data['dictionary']
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

The ``quality_report`` isn't strictly required by VERTEX, and is thus empty.

.. code:: python

   >>> vertex_static_data['quality_report']
   {}

These dataframes can be exported to input CSVs (via the :py:meth:`pandas.DataFrame.to_csv` method) in order to set up a static VERTEX dashboard. For the example presented above, the CSVs can be named as follows:

* ``df_map.csv`` - a CSV export of ``vertex_static_data["df_map"]``
* ``daily.csv`` - a CSV export of ``vertex_static_data["daily"]``
* ``presentation.csv`` - a CSV export of ``vertex_static_data["presentation"]
* ``observation.csv`` - a CSV export ``vertex_static_data["during_observation"]
* ``outcome.csv`` - a CSV export of ``vertex_static_data["outcome"]

Please refer to the :ref:`VERTEX project <isaric-vertex:project-structure>` for more information on how to structure these files for VERTEX dashboard visualisation.

.. _vertex-outputs-from-isaric-data-schema:

From ISARIC Data Schema
+++++++++++++++++++++++

VERTEX outputs can also be obtained if you already have data in ISARIC data schema format via the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_vertex` function, as shown in the snippet below.

.. code:: python

   >>> import warnings; warnings.filterwarnings('ignore')
   >>> vertex_static_data = transform_to_vertex(ids_tables['core'], ids_tables['long'], arc_version='v1.6.1')
