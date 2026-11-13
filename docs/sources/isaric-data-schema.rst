.. _isaric-data-schema:

==================
ISARIC Data Schema
==================

This is a brief guide to the :py:mod:`isaricanalytics.isaric_data_schema` library, which supports direct transformations of raw, custom clinical datasets into the standardised :doc:`ISARIC data schema <isaric-arc:sources/isaric-data-schema>` format, which can be analysed and visualised without much effort.

Before proceeding further, it is recommended to consult the ARC :doc:`ISARIC data schema guide <isaric-arc:sources/isaric-data-schema>` for more information on the core table (one-row-per-patient) and long table (multiple-rows-per-patient) output formats, and the required columns within each table, and also the ARC :doc:`parser guide <isaric-arc:sources/writing-a-parser>` on how to write the parser file.

.. _schema-transformation-pipeline:

The Schema Transformation Pipeline
----------------------------------

The main transformation pipeline, that converts a raw, custom clinical dataset with an associated parser file to the ISARIC data schema format, is implemented by  :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema`. This function can produce either the basic ISARIC data schema outputs, which are the core and long tables, or, optionally, VERTEX-style, analysis-ready outputs, as described below.

.. _schema-transformation-basic:

Basic Schema Outputs
~~~~~~~~~~~~~~~~~~~~

To produce the basic ISARIC data schema outputs call the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function with two required arguments:

* ``parser_file`` - the (relative or absolute) file path of **TOML parser file** that describes how columns in the source dataset map to columns in the core or long table versions of the ISARIC data schema. If both core and long table outputs are required the parser file will need to define both sets of mappings.

* ``data_file`` - the (relative or absolute) file path of the **CSV data file** containing the raw data.

There is an optional ``arc_version`` argument that takes ARC release version strings of the form ``"vX.Y.Z"`` - if this is null the latest version will be fetched.

Example parser and custom (synthetic) datasets have been added `here <https://github.com/ISARICResearch/IsaricAnalytics/tree/ids-refactoring/docs/examples>`_. Below is an example run of the main transform pipeline with the COVID-19 example dataset and parser:

.. code:: python

   >>> import warnings; warnings.filterwarnings('ignore')
   >>> from isaricanalytics.isaric_data_schema import *
   >>> tables = transform_to_isaric_data_schema('./docs/examples/covid19_arc_v1.6.1_example_parser.toml', './docs/examples/covid19_arc_v1.6.1_example_data.csv', 'v1.6.1')
   [covid-study] parsing covid19_arc_v1.6.1_example_data.csv: 100%|███████████████████████████████████████| 5/5 [00:00<00:00, 53.91it/s]
   [covid-study] validating core table: 5it [00:00, 54330.36it/s]
   [covid-study] validating long table: 109it [00:00, 191208.34it/s]
   2026-11-11 11:45:48 [INFO] arc.arc_core: version: v1.6.1

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
   [covid-study] parsing covid19_arc_v1.6.1_example_data.csv: 100%|██████████████████████████████████████| 5/5 [00:00<00:00, 575.63it/s]
   [covid-study] validating core table: 5it [00:00, 33554.43it/s]
   [covid-study] validating long table: 109it [00:00, 205658.63it/s]
   /Users/smurthy/Documents/srm/dev/ISARICAnalytics/src/isaricanalytics/isaric_data_schema.py:252: DeprecationWarning:

   The following core table columns are not in ARC v1.6.1: "adtl_error", "adtl_valid", "dataset_disease", "dataset_id", "demog_age_days", "demog_country_iso3", "siteid"

   Please check these columns.
     _warn_on_non_arc_columns(
   /Users/smurthy/Documents/srm/dev/ISARICAnalytics/src/isaricanalytics/isaric_data_schema.py:258: DeprecationWarning:

   The following long table columns are not in ARC v1.6.1: "adtl_valid", "arcver", "attribute", "attribute_status", "attribute_unit", "dataset_id", "date", "duration", "phase", "value", "value_num"

   Please check these columns.
     _warn_on_non_arc_columns(
   /Users/smurthy/Documents/srm/dev/ISARICAnalytics/src/isaricanalytics/isaric_data_schema.py:271: DeprecationWarning:

   The following source columns are not mapped to any core or long table columns: "ethnic", "icu_in", "icu_out", "icu_treat_antiviral_agents", "icu_treat_corticosteroids", "treat_antiviral_agents", "treat_corticosteroids"

   Please check these columns.
     _warn_on_non_mapped_source_columns(non_mapped_source_columns)
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

To turn the warnings off in the Python session filter out warnings again.

.. code:: python

   >>> warnings.filterwarnings('always')

.. _schema-transformation-vertex-outputs:

VERTEX-style Outputs
~~~~~~~~~~~~~~~~~~~~

If you're a `VERTEX <https://vertex.isaric.org>`_ user, and interested in writing insight panels for a VERTEX dashboard, then you will need VERTEX-compatible dataframes representing one-row-per-patient data, as well as multi-row-per-patient observations data organised by date or event ID and patient interaction phase, and also the corresponding VERTEX data dictionary. This can be done in two ways depending on the format of the source data, as described below.

.. _vertex-outputs-from-raw-data:

From Raw Data
+++++++++++++

With the additional optional argument of ``as_vertex_data=True`` the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` function will return a dictionary of data required for VERTEX dashboard visualisation, as shown in the snippet below.

.. code:: python

   >>> import warnings; warnings.filterwarnings('ignore')
   >>> vertex_data = transform_to_isaric_data_schema('./docs/examples/covid19_arc_v1.6.1_example_parser.toml', './docs/examples/covid19_arc_v1.6.1_example_data.csv', as_vertex_data=True)
   [covid-study] parsing covid19_arc_v1.6.1_example_data.csv: 100%|███████████████████████████████████████| 5/5 [00:00<00:00, 52.66it/s]
   [covid-study] validating core table: 5it [00:00, 55043.36it/s]
   [covid-study] validating long table: 109it [00:00, 192577.56it/s]
   2026-11-11 12:46:14 [INFO] arc.arc_core: version: v1.6.1
   INFO:arc.arc_core:version: v1.6.1
   >>> vertex_data.keys()
   dict_keys(['df_map', dictionary', 'df_forms_dict', 'quality_report'])

The transformation pipeline here works almost identically to non-VERTEX output option, except that there are additional steps to build the VERTEX-specific data, including ``df_map``, the VERTEX data dictionary (``dictionary``) and the forms data (``df_forms_dict``). The first and most important of these is named ``"df_map"``, which contains only one-row-per-patient data, organised by the ``dataset_id`` and ``subjid`` columns:

.. code:: python

   >>> vertex_data['df_map']
     subjid       siteid   dataset_id dataset_disease  ... demog_age_units  inclu_disease outco_binary_outcome         site
   0   C001  SITE-GBR-01  COVID-STUDY        COVID-19  ...           Years       COVID-19           Discharged  COVID-STUDY
   1   C002  SITE-DEU-01  COVID-STUDY        COVID-19  ...           Years       COVID-19                Death  COVID-STUDY
   2   C003  SITE-USA-01  COVID-STUDY        COVID-19  ...           Years       COVID-19           Discharged  COVID-STUDY
   3   C004  SITE-GBR-02  COVID-STUDY        COVID-19  ...           Years       COVID-19                  NaN  COVID-STUDY
   4   C005  SITE-ESP-01  COVID-STUDY        COVID-19  ...           Years       COVID-19                  NaN  COVID-STUDY

   [5 rows x 40 columns]

The VERTEX dictionary is available via the ``'dictionary'`` key:

.. code:: python

   >>> vertex_data['dictionary']
                              field_name     form_name   field_type            field_label                parent branching_logic
   0                               study  presentation      section                  STUDY
   1                               demog  presentation      section           DEMOGRAPHICS
   2                                pres  presentation      section   ONSET & PRESENTATION
   3                               outco       outcome      section                OUTCOME
   4                               adsym  presentation      section  SYMPTOMS ON ADMISSION
   ..                                ...           ...          ...                    ...                   ...             ...
   70       outco_binary_outcome___Death       outcome       binary                  Death  outco_binary_outcome
   71  outco_binary_outcome___Discharged       outcome       binary             Discharged  outco_binary_outcome
   72    outco_binary_outcome___Censored       outcome       binary               Censored  outco_binary_outcome
   73                               site  presentation  categorical                   Site                 study
   74                 site___COVID-STUDY  presentation       binary            COVID-STUDY                  site

   [75 rows x 6 columns]

The forms data is available via the ``'df_forms_dict'`` key, and is a dict organised by date or event ID, and patient interaction phase:

.. code:: python

   >>> vertex_data['df_forms_dict'].keys()
   dict_keys(['during_observation_date', 'outcome_date', 'presentation_date'])

For this example dataset there are no event ID based observations, only date based observations.

.. code:: python

   >>> vertex_data['df_forms_dict']['presentation_date']
   value subjid        date attribute_status arcver   dataset_id  ... attribute_unit value_num duration  _unit  _value _duration
   0     Yes   C001  2023-01-10              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN      NaN            Yes       NaN
   1     Yes   C001  2023-01-10              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN      NaN            Yes       NaN
   2     Yes   C001  2023-01-10              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN      NaN            Yes       NaN
   3      No   C001  2023-01-10              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN      NaN             No       NaN
   4     Yes   C001  2023-01-10              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN      NaN            Yes       NaN
   ..    ...    ...         ...              ...    ...          ...  ...            ...       ...      ...    ...     ...       ...
   97    NaN   C005  2023-01-14              VAL  1.6.1  COVID-STUDY  ...            NaN      82.0      NaN           82.0       NaN
   98    NaN   C005  2023-01-14              VAL  1.6.1  COVID-STUDY  ...            NaN      20.0      NaN           20.0       NaN
   99    NaN   C005  2023-01-14              VAL  1.6.1  COVID-STUDY  ...            NaN      95.0      NaN           95.0       NaN
   100   NaN   C005  2023-01-14              VAL  1.6.1  COVID-STUDY  ...            NaN     132.0      NaN          132.0       NaN
   101   NaN   C005  2023-01-14              VAL  1.6.1  COVID-STUDY  ...            NaN      82.0      NaN           82.0       NaN

   [69 rows x 14 columns]
   >>>
   >>> vertex_data['df_forms_dict']['during_observation_date']
   value subjid        date attribute_status arcver   dataset_id  ... attribute_unit value_num duration  _unit  _value _duration
   40   Yes   C002  2023-01-13              VAL  1.6.1  COVID-STUDY  ...            NaN       NaN     12.0            Yes      12.0

   [1 rows x 14 columns]
   >>>
   >>> vertex_data['df_forms_dict']['outcome_date']
         value subjid        date attribute_status arcver  ... value_num duration   _unit     _value  _duration
   14         NaN   C001  2023-01-17              VAL  1.6.1  ...      42.3      NaN    mg/L       42.3        NaN
   15         NaN   C001  2023-01-17              VAL  1.6.1  ...       1.2      NaN  10^9/L        1.2        NaN
   16         NaN   C001  2023-01-17              VAL  1.6.1  ...       7.8      NaN  10^9/L        7.8        NaN
   17          No   C001  2023-01-17              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   19          No   C001  2023-01-17              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   20          No   C001  2023-01-17              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   34         NaN   C002  2023-01-28              VAL  1.6.1  ...     187.6      NaN    mg/L      187.6        NaN
   35         NaN   C002  2023-01-28              VAL  1.6.1  ...       0.4      NaN  10^9/L        0.4        NaN
   36         NaN   C002  2023-01-28              VAL  1.6.1  ...      12.3      NaN  10^9/L       12.3        NaN
   39         Yes   C002  2023-01-28              VAL  1.6.1  ...       NaN      NaN                Yes        NaN
   41         Yes   C002  2023-01-28              VAL  1.6.1  ...       NaN      NaN                Yes        NaN
   42         Yes   C002  2023-01-28              VAL  1.6.1  ...       NaN      NaN                Yes        NaN
   43   Bacterial   C002  2023-01-28              VAL  1.6.1  ...       NaN      NaN          Bacterial        NaN
   58         NaN   C003  2023-01-19              VAL  1.6.1  ...      28.7      NaN    mg/L       28.7        NaN
   59         NaN   C003  2023-01-19              VAL  1.6.1  ...       0.9      NaN  10^9/L        0.9        NaN
   60         NaN   C003  2023-01-19              VAL  1.6.1  ...       8.1      NaN  10^9/L        8.1        NaN
   62         Yes   C003  2023-01-19              VAL  1.6.1  ...       NaN      NaN                Yes        NaN
   64          No   C003  2023-01-19              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   65          No   C003  2023-01-19              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   102        NaN   C005  2023-01-21              VAL  1.6.1  ...      67.8      NaN    mg/L       67.8        NaN
   103        NaN   C005  2023-01-21              VAL  1.6.1  ...       1.1      NaN  10^9/L        1.1        NaN
   104        NaN   C005  2023-01-21              VAL  1.6.1  ...       9.2      NaN  10^9/L        9.2        NaN
   105         No   C005  2023-01-21              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   107         No   C005  2023-01-21              VAL  1.6.1  ...       NaN      NaN                 No        NaN
   108         No   C005  2023-01-21              VAL  1.6.1  ...       NaN      NaN                 No        NaN

   [25 rows x 14 columns]

The quality report is more specific to REDCap-based projects in legacy versions of VERTEX, and is thus empty for the data schema transform pipeline.

.. code:: python

   >>> vertex_data['quality_report']
   {}

These dataframes can be exported to input CSVs (via the :py:meth:`pandas.DataFrame.to_csv` method) in order to set up a static VERTEX dashboard. For the example presented above, the CSVs can be named as follows:

* ``df_map.csv`` - a CSV export of ``vertex_data["df_map"]``
* ``presentation.csv`` - a CSV export of ``vertex_data["df_forms_dict"]["presentation_date"]``
* ``observation.csv`` - a CSV export ``vertex_data["df_forms_dict"]["during_observation_date"]``
* ``outcome.csv`` - a CSV export of ``vertex_data["df_forms_dict"]["outcome_date"]``

Please refer to the :ref:`VERTEX project <isaric-vertex:project-structure>` for more information on how to structure these files for VERTEX dashboard visualisation.

.. _vertex-outputs-from-isaric-data-schema:

From ISARIC Data Schema
+++++++++++++++++++++++

VERTEX outputs can also be obtained directly from the core and long tables via the :py:func:`~isaricanalytics.isaric_data_schema.transform_to_vertex` function, as shown in the snippet below.

.. code:: python

   >>> import warnings; warnings.filterwarnings('always')
   >>> vertex_data = transform_to_vertex(ids_tables['core'], ids_tables['long'], arc_version='v1.6.1')
   >>> vertex_data.keys()
   dict_keys(['df_map', 'dictionary', 'df_forms_dict', 'quality_report'])

This function produces the same data as calling :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema` with the ``as_vertex_data=True`` option.

Note that, as with :py:func:`~isaricanalytics.isaric_data_schema.transform_to_isaric_data_schema`, the ``arc_version`` is purely optional - if this is null the latest release version will be fetched from ARC.
