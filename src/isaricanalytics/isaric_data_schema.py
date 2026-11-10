from __future__ import annotations

__all__ = [
    "clean_arc_data_dictionary",
    "clean_observations",
    "get_attribute_arc_source_map",
    "get_attribute_duration_observations",
    "get_attribute_observations",
    "get_attribute_unit_observations",
    "get_date_observations_by_phase",
    "get_event_observations_by_phase",
    "get_observations",
    "get_parser_source_field_map",
    "get_parser_toml_map",
    "get_vertex_data_dictionary",
    "get_vertex_data",
    "get_vertex_df_forms_proxy",
    "get_vertex_df_map_proxy",
    "get_wide_observations_table",
    "transform_to_isaric_data_schema",
    "transform_to_vertex",
]


# -- IMPORTS --

# -- Standard libraries --
import importlib.resources
import json
import pathlib
import tomllib
import typing
import warnings as warnings_
from itertools import chain, product

# -- External libraries --
import adtl
import pandas as pd
from arc.arc_api import ArcApiClient, ArcApiClientError
from arc.arc_core import get_arc

# -- Internal libraries --
import isaricanalytics.isaric_transformations as tf

ASSETS = importlib.resources.files("isaricanalytics") / "assets"


class IsaricDataSchemaTransformationException(Exception):
    """Base exception class for the ISARIC data schema library."""


def _warn_on_non_arc_columns(
    column_set: typing.Iterable, column_type: str, arc_version: str, stacklevel=2
) -> None:
    """Warns on the transform function detecting non-ARC columns in the core or long schema tables."""  # noqa: E501
    columns_str = ", ".join(map(lambda s: f'"{s}"', sorted(column_set)))
    msg = (
        f"\n\nThe following {column_type} table columns are not in ARC "
        f"{arc_version}: {columns_str}\n\nPlease check these columns."
    )
    warnings_.warn(msg, DeprecationWarning, stacklevel=stacklevel)


def _warn_on_non_mapped_source_columns(
    column_set: typing.Iterable, stacklevel=2
) -> None:
    """Warns on the transform function detecting source columns that are not mapped to any core or long table column."""  # noqa: E501
    columns_str = ", ".join(map(lambda s: f'"{s}"', sorted(column_set)))
    msg = (
        f"\n\nThe following source columns are not mapped to any core or "
        f"long table columns: {columns_str}\n\nPlease check these columns."
    )
    warnings_.warn(msg, DeprecationWarning, stacklevel=stacklevel)


def get_parser_toml_map(parser_file: str | pathlib.Path, /) -> dict[str, typing.Any]:
    """:py:class:`dict` : The parser TOML as a map/dict.

    Parameters
    ----------
    parser_file : str or pathlib.Path
        The (relative or absolute) parser file path.

    Returns
    -------
    dict
        The parser TOML as a map/dict.
    """
    with pathlib.Path(parser_file).resolve().open(mode="rb") as fp:
        return tomllib.load(fp)


def get_parser_source_field_map(
    parser_file: str | pathlib.Path, /
) -> dict[str, tuple[str]]:
    """:py:class:`dict` : Returns a map of the source fields defined in the parser, organised by table type.

    Parameters
    ----------
    parser_file : str or pathlib.Path
        The (relative or absolute) parser file path.

    Returns
    -------
    dict
        The source fields defined in the parser file, organised by table
        type.
    """  # noqa : E501
    # Get the parser TOML as a map
    toml_map = get_parser_toml_map(parser_file)

    # Define the source field map as a dict with two entries: one for the core
    # table columns, and the other for the long table columns,  with the initial
    # value of each set to an empty list, to allow for iterative updates.
    source_field_map = {"core": [], "long": []}
    toml_core = toml_map["core"]
    toml_long = toml_map["long"]

    # A preliminary step to build an iterable of field definition items for
    # both the core and long tables, which can vary depending on whether the
    # source tables from the TOML map are dicts or lists (JSON arrays).
    core_table_field_defs = (
        product(["core"], toml_core.items())
        if isinstance(toml_core, dict)
        else product(["core"], toml_core)
    )
    long_table_field_defs = (
        product(["long"], toml_long.items())
        if isinstance(toml_long, dict)
        else product(["long"], toml_long)
    )

    # The main loop over a combined sequence of core and long table column
    # definitions: for each column definition extract the source field and
    # update the corresponding list in the source field map.
    for table_type, item in chain(core_table_field_defs, long_table_field_defs):
        if isinstance(item, tuple):
            key, value = item
            if isinstance(value, dict) and value.get("field"):
                source_field_map[table_type].append(value["field"])
        elif isinstance(item, dict):
            if "value" in item and item["value"].get("field"):
                source_field_map[table_type].append(item["value"]["field"])
            elif "value_num" in item and item["value_num"].get("field"):
                source_field_map[table_type].append(item["value_num"]["field"])
        else:
            continue

    # A post-processing step to ensure that the source columns in the source
    # field map are immutable, before returning.
    source_field_map["core"] = tuple(source_field_map["core"])
    source_field_map["long"] = tuple(source_field_map["long"])

    return source_field_map


def transform_to_isaric_data_schema(
    parser_file: str | pathlib.Path,
    data_file: str | pathlib.Path,
    /,
    *,
    arc_version: str | None = None,
    as_vertex_data: bool = False,
) -> dict[str, pd.DataFrame]:
    """:py:class:`dict` : ISARIC schema-compliant short/core- and long-format datasets as Pandas dataframes, with optional VERTEX-style output.

    Parameters
    ----------
    parser_file : str or pathlib.Path
        The parser TOML file path.

    data_file : str or pathlib.Path
        The data file path.

    arc_version : str or None, default=None
        Optional ARC version string used to fetch the ARC data dictionary
        associated with the ARC version; defaults to ``None`` in which
        case the latest ARC version is used.

    as_vertex_data : bool, default=False
        Optional indicator of whether to return the data as a VERTEX-style
        dictionary in the format:
        ::

            {
                "df_map": <one-row-per-patient dataframe>,
                "df_forms_dict": <dict of patient observations dataframes keyed by interaction phase>,
                "vertex_dictionary": <VERTEX data dictionary>,
                "quality_report": <quality report>
            }

    Returns
    -------
    dict
        A dict of the form:
        ::

            {
                "core": <ISARIC data schema core table>,
                "long": <ISARIC data schema long table>
            }

        or, if ``as_vertex_data``:
        ::

            {
                "df_map": <one-row-per-patient dataframe>,
                "df_forms_dict": <dict of patient observations dataframes (unit attributes, duration attributes)  interaction phase>,
                "vertex_dictionary": <VERTEX data dictionary>,
                "quality_report": <quality report>
            }
    Raises
    ------
    IsaricDataSchemaTransformationException
        In case of an ARC API client exception.
    """  # noqa : E501
    # Call ADTL to parse the data and retrieve the core and long-format tables.
    ids_tables = adtl.parse(parser_file, data_file, include_transform=tf.__file__)
    core = ids_tables["core"]
    long_ = ids_tables["long"]

    # An ARC version is required to fetch the ARC data dictionary. If no ARC
    # version is provided by the caller, fetch the latest directly from ARC @
    # GitHub - in case of an exception raise it.
    if not arc_version:
        try:
            arc_version = ArcApiClient().get_arc_version_list()[0]
        except (ArcApiClientError, IndexError) as e:
            raise IsaricDataSchemaTransformationException(
                f'Exception fetching ARC version "{arc_version}": '
                f"{e}.\n\n Please check that you have provided a valid "
                "ARC version. If you have then there may be a network- "
                "related error, so please retry after some time."
            )

    # Fetch the ARC data dictionary associated with the ARC version - in case
    # of an exception raise it.
    try:
        arc_dd = get_arc(arc_version)[0]
    except (ArcApiClientError, IndexError) as e:
        raise IsaricDataSchemaTransformationException(
            "Exception fetching ARC data dictionary for ARC version "
            f'"{arc_version}": {e}.\n\n Please check that you have provided a '
            "valid ARC version. If you have, then please retry after some "
            "time."
        )

    # Checking transformed columns in the core and long tables against ARC, and
    # issuing warnings about any non-ARC columns in either.
    non_arc_core_columns = set(core.columns).difference(arc_dd["Variable"])
    if non_arc_core_columns:
        _warn_on_non_arc_columns(
            non_arc_core_columns, "core", arc_version, stacklevel=2
        )

    non_arc_long_columns = set(long_.columns).difference(arc_dd["Variable"])
    if non_arc_long_columns:
        _warn_on_non_arc_columns(
            non_arc_long_columns, "long", arc_version, stacklevel=2
        )

    # Checking the source file for any columns that are not mapped to data
    # columns in the parser file, and in that case issuing warnings.
    parser_source_field_map = get_parser_source_field_map(parser_file)
    toml_source_fields = set(parser_source_field_map["core"]).union(
        parser_source_field_map["long"]
    )
    src_data = pd.read_csv(data_file)
    non_mapped_source_columns = set(src_data.columns).difference(toml_source_fields)
    if non_mapped_source_columns:
        _warn_on_non_mapped_source_columns(non_mapped_source_columns)

    if not as_vertex_data:
        return ids_tables

    vertex_data = get_vertex_data(core, long_, arc_dd)

    return {
        **vertex_data,
        **{"quality_report": {}},
    }


def transform_to_vertex(
    isaric_core_table: pd.DataFrame,
    isaric_long_table: pd.DataFrame,
    /,
    *,
    arc_version: str | None = None,
) -> dict[str, typing.Any]:
    """:py:class:`dict` : A dict of VERTEX-compatible dataframes for analytics.

    Parameters
    ----------
    isaric_core_table : pandas.DataFrame
        The ISARIC data schema core table.

    isaric_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    arc_version : str or None, default=None
        Optional ARC version string used to fetch the ARC data dictionary
        associated with the ARC version; defaults to ``None`` in which
        case the latest ARC version is used.

    Returns
    -------
    dict
        VERTEX dataframes in a dict of the form:
        ::

            {
                "df_map": <one-row-per-patient dataframe>,
                "daily": <patient observations dataframe>,
                "dictionary": <ARC data dictionary>
            }
    """  # noqa : E501
    # An ARC version is required to fetch the ARC data dictionary. If no ARC
    # version is provided by the caller, fetch the latest directly from ARC @
    # GitHub - in case of an exception raise it.
    core = isaric_core_table
    long_ = isaric_long_table

    if not arc_version:
        try:
            arc_version = ArcApiClient().get_arc_version_list()[0]
        except (ArcApiClientError, IndexError) as e:
            raise IsaricDataSchemaTransformationException(
                f'Exception fetching ARC version "{arc_version}": '
                f"{e}.\n\n Please check that you have provided a valid "
                "ARC version. If you have then there may be a network- "
                "related error, so please retry after some time."
            )

    # Fetch the ARC data dictionary associated with the ARC version - in case
    # of an exception raise it.
    try:
        arc_dd = get_arc(arc_version)[0]
    except (ArcApiClientError, IndexError) as e:
        raise IsaricDataSchemaTransformationException(
            "Exception fetching ARC data dictionary for ARC version "
            f'"{arc_version}": {e}.\n\n Please check that you have provided a '
            "valid ARC version. If you have, then please retry after some "
            "time."
        )

    vertex_data = get_vertex_data(
        core,
        long_,
        arc_dd,
    )

    return {
        **vertex_data,
        **{"quality_report": {}},
    }


def get_vertex_data(
    isaric_core_table: pd.DataFrame,
    isaric_long_table: pd.DataFrame,
    arc_data_dictionary: pd.DataFrame,
    /,
) -> dict[str, typing.Any]:
    """:py:class:`dict` : Returns a dict of VERTEX data including ``df_map`` proxy and data dictionary.

    Parameters
    ----------
    isaric_core_table : pandas.DataFrame
        The ISARIC data schema core table.

    isaric_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    arc_data_dictionary : pandas.DataFrame
        ARC data dictionary.

    Raises
    ------
    IsaricDataSchemaTransformationException
        In case of exceptions in some of the key transformation steps.

    Returns
    -------
    dict
        A dict of VERTEX data, including the ``df_map`` proxy, the VERTEX
        dictionary, and the ``df_forms_dict``:
        ::

            {
                "df_map": <>,
                "dictionary": vertex_dictionary,
                "df_forms_dict": df_forms
            }
    """  # noqa : E501
    core = isaric_core_table.drop(
        columns=[col for col in isaric_core_table.columns if col.startswith("adtl")]
    )
    long_ = isaric_long_table.drop(
        columns=[col for col in isaric_long_table.columns if col.startswith("adtl")]
    ).drop_duplicates()

    try:
        # Get cleaned/preprocessed observations from the long table.
        observations = get_observations(long_)

        # Construct a "wide" table of observations with the necessary additional
        # columns representing individual attributes.
        patient_keys = ["dataset_id", "subjid"]
        wide = get_wide_observations_table(core, observations, patient_keys)

        # Construct initial df_map with all the columns expected by VERTEX.
        df_map = get_vertex_df_map_proxy(core, wide, patient_keys)

        # Map attribute/unit and attribute/duration columns in df_map to their
        # ARC source values.
        attr_source_map = get_attribute_arc_source_map(df_map, observations)

        # Clean the ARC data dictionary for df_map, preserving ARC's original
        # form groups.
        arc_dd = clean_arc_data_dictionary(arc_data_dictionary)

        # Create VERTEX data dictionary.
        vertex_dd = get_vertex_data_dictionary(df_map, arc_dd, attr_source_map)

        # Create the df_forms dict
        df_forms = get_vertex_df_forms_proxy(observations)
    except ValueError as e:
        raise IsaricDataSchemaTransformationException(e)

    return {"df_map": df_map, "dictionary": vertex_dd, "df_forms_dict": df_forms}


def get_vertex_df_forms_proxy(observations: pd.DataFrame, /) -> dict[str, pd.DataFrame]:
    """:py:class:`pandas.DataFrame` : Returns a proxy for the VERTEX ``df_forms`` dict containing a dataframe of patient interaction data for each patient interaction phase/state.

    Parameters
    ----------
    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    Returns
    -------
    dict
        A dict of long table single-attribute observations dataframes,
        organised by (attribute/unit)_phase and (attribute/duration)_phase.
    """  # noqa : E501
    # Get dicts of date-based and event-based observations organised by phase,
    # and merge the two dicts.
    date_observations = get_date_observations_by_phase(observations)

    # A step to deal with observations that have no ``event_id`` based rows.
    try:
        event_observations = get_event_observations_by_phase(observations)
    except ValueError:
        return date_observations

    # Merge the two dicts and return.
    return {**date_observations, **event_observations}


def clean_observations(observations: pd.DataFrame, /) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Cleans/preprocesses the observations from the long table.

    Parameters
    ----------
    observations : pandas.DataFrame
        The unprocessed ISARIC long table.

    Returns
    -------
    pandas.DataFrame
        The cleaned observations data.
    """  # noqa : E501
    for column in ("attribute_unit", "value", "value_num", "duration"):
        if column not in observations.columns:
            observations[column] = pd.NA

        observations[column] = observations[column].replace(r"^\s*$", pd.NA, regex=True)

    observations["_unit"] = (
        observations["attribute_unit"].fillna("").astype(str).str.strip()
    )
    observations["_value"] = observations["value"].combine_first(
        observations["value_num"]
    )
    observations["_duration"] = observations["duration"]

    return observations


def get_observations(isaric_long_table: pd.DataFrame, /) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns a dataframe of cleaned and deduplicated observations from the ISARIC long table.

    Parameters
    ----------
    isaric_long_table : pandas.DataFrame
        The unprocessed ISARIC long table.

    Returns
    -------
    pandas.DataFrame
        Cleaned and deduplicated rows from the long table representing
        individual observations.
    """  # noqa : E501
    return clean_observations(get_attribute_observations(isaric_long_table))


def get_attribute_observations(isaric_long_table: pd.DataFrame, /) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame : Returns a long table with one row per attribute per observation per patient.

    Parameters
    ----------
    isaric_long_table : pandas.DataFrame
        The unprocessed ISARIC long table.

    Returns
    -------
    pandas.DataFrame
        A long table with one row per attribute per observation per patient.
    """  # noqa : E501
    # Start by dropping duplicate rows.
    long_ = isaric_long_table.drop_duplicates()

    # Count observations per patient and attribute.
    counts = long_.groupby(
        ["dataset_id", "subjid", "attribute"],
        dropna=False,
    ).size()

    # An attribute qualifies for inclusion only if no patient has multiple
    # observations.
    maximum_count = counts.groupby(level="attribute").max()
    eligible_attributes_dfmap = maximum_count[maximum_count <= 1].index

    # Subset the long table to only those attributes that are eligible for
    # inclusion in the df_map (happening exactly once per patient in the
    # observation period.
    return long_.loc[long_["attribute"].isin(eligible_attributes_dfmap)].copy()


def get_attribute_unit_observations(
    observations: pd.DataFrame, patient_keys: list[str]
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns patient attribute/unit observations data.

    Parameters
    ----------
    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    patient_keys : list
        A list of columns defining patient keys.

    Returns
    -------
    pandas.DataFrame
        Attribute/unit observations data as a single dataframe.
    """  # noqa : E501
    # Define the pivot columns
    pivot_columns = [
        "attribute",
        "_unit",
    ]

    # Perform the pivot, create the unit attribute suffixed columns on
    # the pivoted dataframe, and return.
    attr_unit_observations = observations.pivot(
        index=patient_keys,
        columns=pivot_columns,
        values="_value",
    )

    attr_unit_observations.columns = [
        f"{attribute}_{unit}" if unit else attribute
        for attribute, unit in attr_unit_observations.columns
    ]

    return attr_unit_observations


def get_attribute_duration_observations(
    observations: pd.DataFrame, patient_keys: list[str]
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns patient attribute/observations data.

    Parameters
    ----------
    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    patient_keys : list
        A list of columns defining patient ID keys.

    Returns
    -------
    pandas.DataFrame
        Attribute/duration observations data as a single dataframe.
    """  # noqa : E501
    # Define the pivot column and extract the duration rows.
    pivot_columns = [
        "attribute",
    ]

    duration_rows = observations.loc[observations["_duration"].notna()]

    # If there are duration rows then pivot on attribute, create the
    # duration-suffixed columns in the pivoted dataframe and return it.
    if not duration_rows.empty:
        attr_duration_observations = duration_rows.pivot(
            index=patient_keys,
            columns=pivot_columns,
            values="_duration",
        )

        attr_duration_observations.columns = [
            f"{attribute}_duration" for attribute in attr_duration_observations.columns
        ]

        return attr_duration_observations

    # Return an empty dataframe if there are no duration rows.
    return pd.DataFrame()


def get_wide_observations_table(
    isaric_core_table: pd.DataFrame,
    observations: pd.DataFrame,
    patient_keys: list[str],
    /,
) -> tuple[pd.DataFrame]:
    """:py:class:`pandas.DataFrame` : A wide observations table that includes attribute/unit and attribute/duration columns.

    Parameters
    ----------
    isaric_core_table : pandas.DataFrame
        The ISARIC core table.

    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    patient_keys : list
        A list of columns to use as patient keys to pivoting.

    Raises
    ------
    ValueError
        In case of ambiguous or overlapping column names.

    Returns
    -------
    pandas.DataFrame
        The wide observations table.
    """  # noqa : E501
    core = isaric_core_table

    # Create wide table initially with the attribute/unit observations
    wide = get_attribute_unit_observations(observations, patient_keys)

    # Create attribute/duration columns
    attr_duration_observations = get_attribute_duration_observations(
        observations, patient_keys
    )
    if not attr_duration_observations.empty:
        wide = pd.concat([wide, attr_duration_observations], axis=1)

    # Prevent ambiguous or overlapping column names.
    if not wide.columns.is_unique:
        raise ValueError("Generated df_map column names are not unique")

    overlaps = sorted(set(wide.columns).intersection(core.columns))
    if overlaps:
        raise ValueError(f"Generated columns overlap core fields: {overlaps}")

    wide.columns.name = None

    return wide


def get_date_observations_by_phase(
    observations: pd.DataFrame, /
) -> dict[str, pd.DataFrame]:
    """:py:class:`dict` : Returns a dict of date-based observations dataframes organised by patient interaction phase.

    Parameters
    ----------
    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    Raises
    ------
    ValueError
        If there are no date-based observations, or no ``"date"`` column in
        the observations.

    Returns
    -------
    dict
        A dict of date-based observations dataframes organised by patient
        interaction phase in the form:
        ::

            {
                "presentation_date": <date-based observations in the presentation phase>,
                "during_observation_date": <date-based observations in the presentation phase>,
                "outcome_date": <date-based observations in the outcome phase>
            }
    """  # noqa : E501
    # Extract the date-based observations, and raise an error if there are none.
    try:
        date_observations = observations[observations["date"].notnull()]

        if date_observations.empty:
            raise ValueError("Expected date-based observations, none found.")
    except KeyError:
        raise ValueError("No 'date' column found in observations.")

    return {
        f"{phase}_date": phase_date_group
        for phase, phase_date_group in date_observations.groupby("phase")
    }


def get_event_observations_by_phase(
    observations: pd.DataFrame, /
) -> dict[str, pd.DataFrame]:
    """:py:class:`dict` : Returns a dict of event-based observations dataframes organised by patient interaction phase.

    Parameters
    ----------
    observations : pandas.DataFrame
        Preprocessed observations data with unpivoted attributes.

    Raises
    ------
    ValueError
        If there are no event-based observations, i.e. no rows with non-null
        ``event_id``, or no ``"event_id"`` column in the observations.

    Returns
    -------
    dict
        A dict of event-based observations dataframes organised by patient
        interaction phase in the form:
        ::

            {
                "presentation_event": <event-based observations in the presentation phase>,
                "during_observation_event": <event-based observations in the presentation phase>,
                "outcome_event": <event-based observations in the outcome phase>
            }
    """  # noqa : E501
    # Extract the event-based observations, and raise an error if there are none.
    try:
        event_observations = observations[observations["event_id"].notnull()]

        if event_observations.empty:
            raise ValueError("Expected date-based observations, none found.")
    except KeyError:
        raise ValueError("No 'event_id' column found in observations.")

    return {
        f"{phase}_date": phase_event_group
        for phase, phase_event_group in event_observations.groupby("phase")
    }


def get_vertex_df_map_proxy(
    isaric_core_table: pd.DataFrame,
    wide_observations_table: pd.DataFrame,
    patient_keys: list[str],
    /,
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : A VERTEX-compatible df_map.

    Parameters
    ----------
    isaric_core_table : pandas.DataFrame
        The ISARIC core table.

    wide_observations_table : pandas.DataFrame
        The augmented observations table with attribute/unit and
        attribute/duration columns.

    patient_keys : list
        Patient keys for pivoting.

    Returns
    -------
    pandas.DataFrame
        An initial VERTEX-style df_map with the minimal expected columns.
    """  # noqa : E501
    core = isaric_core_table
    wide = wide_observations_table

    # Convert patient identifiers from the index into columns,
    # then attach the observations to every core record.
    df_map = core.merge(
        wide.reset_index(),
        on=patient_keys,
        how="left",
        validate="one_to_one",
    )

    df_map["country_iso"] = df_map["demog_country_iso3"]
    # Convert age in days to approximate years.
    df_map["demog_age"] = (
        pd.to_numeric(df_map["demog_age_days"], errors="coerce") / 365.25
    )
    df_map["demog_age_units"] = "Years"
    df_map["inclu_disease"] = df_map["dataset_disease"]
    outcome = df_map["outco_outcome"].astype("string").str.strip()
    df_map["outco_binary_outcome"] = outcome.map(
        {"Discharged alive": "Discharged", "Death": "Death", "": "Censored"}
    )
    df_map.loc[outcome.isna(), "outco_binary_outcome"] = "Censored"
    df_map["site"] = df_map["dataset_id"]

    for column in df_map.columns:
        values = df_map[column].astype("string").str.strip().str.lower()
        non_missing = values.dropna()

        if not non_missing.empty and non_missing.isin(["yes", "no"]).all():
            df_map[column] = values.map({"yes": True, "no": False})

    return df_map


def get_attribute_arc_source_map(
    df_map: pd.DataFrame,
    observations: pd.DataFrame,
    /,
) -> dict[str, tuple[typing.Any]]:
    """:py:class:`dict` : Attribute field source map for attribute/unit and attribute/duration columns in df_map.

    Parameters
    ----------
    df_map : pandas.DataFrame
        A df_map with attribute/unit and attribute/duration columns.

    observations : pandas.DataFrame
        The cleaned observations data.

    Returns
    -------
    dict
        A dict mapping attribute/unit and attribute/duration columns in df_map
        to ARC values.
    """  # noqa : E501
    duration_rows = observations.loc[observations["_duration"].notna()]
    attr_source_map = {column: (column, "", False) for column in df_map.columns}

    for attribute, unit in (
        observations[["attribute", "_unit"]]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    ):
        column = f"{attribute}_{unit}" if unit else attribute

        if column in df_map.columns:
            attr_source_map[column] = (attribute, unit, False)

    for attribute in duration_rows["attribute"].drop_duplicates():
        column = f"{attribute}_duration"

        if column in df_map.columns:
            attr_source_map[column] = (attribute, "", True)

    return attr_source_map


def clean_arc_data_dictionary(arc_data_dictionary: pd.DataFrame, /) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Cleans the ARC data dictionary.

    The cleaning is minimal, but could potentially be expanded in the future.

    Parameters
    ----------
    arc_data_dictionary : pandas.DataFrame
        The incoming, uncleaned ARC data dictionary.

    Raises
    ------
    ValueError
        If there are duplicate variables.

    Returns
    -------
    pandas.DataFrame
        The cleaned ARC data dictionary/
    """  # noqa : E501
    arc_dd = arc_data_dictionary.fillna("").set_index("Variable")

    # Should this be a warning instead? Duplicate variable rows can be dropped.
    if not arc_dd.index.is_unique:
        raise ValueError("ARC data dictionary contains duplicate Variable names.")

    return arc_dd


def get_vertex_data_dictionary(
    df_map: pd.DataFrame,
    arc_data_dictionary: pd.DataFrame,
    attribute_source_map: dict[str, tuple[typing.Any]],
    /,
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Creates and returns a VERTEX-compatible data dictionary.

    Parameters
    ----------
    df_map : pandas.DataFrame
        A df_map with attribute/unit and attribute/duration columns.

    arc_data_dictionary : pandas.DataFrame
        ARC data dictionary.

    attribute_source_map : dict
        Attribute field source map for attribute/unit and attribute/duration
        columns in df_map.

    Raises
    ------
    ValueError
        In case of duplication variable names in ARC data dictionary.
    """  # noqa : E501
    arc_dd = arc_data_dictionary
    attr_source_map = attribute_source_map
    extra_metadata = json.loads(ASSETS.joinpath("extra_metadata.json").read_text())
    type_map = json.loads(ASSETS.joinpath("type_map.json").read_text())
    dictionary_columns = [
        "field_name",
        "form_name",
        "field_type",
        "field_label",
        "parent",
        "branching_logic",
    ]

    rows = []
    sections = {}

    for column in df_map.columns:
        source, unit, is_duration = attr_source_map[column]

        if column in extra_metadata:
            (
                form,
                field_type,
                label,
                parent,
                section_label,
            ) = extra_metadata[column]
        elif source in arc_dd.index:
            metadata = arc_dd.loc[source]
            form = metadata["Form"]
            label = metadata["Question"]
            parent = source.split("_", 1)[0] if "_" in source else ""
            section_label = metadata["Section"].split(": ", 1)[0] or parent.upper()
            arc_type = metadata["Type"]
            validation = metadata["Validation"]
            choice_labels = {
                option.partition(",")[2].strip().casefold()
                for option in metadata["Answer Options"].split("|")
                if "," in option
            }
            field_type = type_map.get(arc_type)

            if source.endswith("_units"):
                field_type = "units"
            elif validation in {"number", "integer"}:
                field_type = "numeric"
            elif validation in {"date_dmy", "datetime_dmy"}:
                field_type = "date"
            elif (
                arc_type in {"radio", "dropdown"}
                and {"yes", "no"}.issubset(choice_labels)
                and choice_labels.issubset({"yes", "no", "unknown"})
            ):
                field_type = "binary"

            if field_type is None:
                raise ValueError(f"Add a dictionary type rule for {source}: {arc_type}")

            if is_duration:
                field_type = "numeric"
                label = f"{label} - duration (days)"
            elif unit and unit.casefold() not in label.casefold():
                label = f"{label} ({unit})"
        else:
            raise ValueError(f"No ARC or additional metadata found for {column}")

        rows.append(
            [
                column,
                form,
                field_type,
                label,
                parent,
                "",
            ]
        )

        # Add the parent section once.
        if parent:
            if parent in df_map.columns:
                raise ValueError(f"Section name conflicts with a data column: {parent}")

            if parent in sections and sections[parent][1] != form:
                raise ValueError(
                    f"Section {parent} occurs in multiple forms; " "define its grouping"
                )

            sections.setdefault(
                parent,
                [parent, form, "section", section_label, "", ""],
            )

        # Ensure binary fields contain booleans or missing values.
        # This also handles a column containing Yes/No/Unknown.
        if field_type == "binary":
            values = df_map[column].astype("string").str.strip().str.casefold()
            allowed = {
                "yes",
                "no",
                "true",
                "false",
                "unknown",
                "not known",
                "",
            }
            invalid = values.notna() & ~values.isin(allowed)

            if invalid.any():
                raise ValueError(f"Unrecognised binary values in {column}")

            df_map[column] = values.map(
                {
                    "yes": True,
                    "no": False,
                    "true": True,
                    "false": False,
                }
            ).astype("boolean")

        # Add category-option metadata using observed labels.
        # This does not create one-hot columns in df_map.
        if field_type in {"categorical", "units"}:
            choices = df_map[column].dropna().astype(str).str.strip()
            choices = choices[choices.ne("")].drop_duplicates().tolist()

            # Preserve the three defined options for the derived outcome.
            if column == "outco_binary_outcome":
                choices = ["Death", "Discharged", "Censored"]

            for choice in choices:
                rows.append(
                    [
                        f"{column}___{choice}",
                        form,
                        "binary",
                        choice,
                        column,
                        "",
                    ]
                )

    vertex_data_dictionary = pd.DataFrame(
        list(sections.values()) + rows,
        columns=dictionary_columns,
    )

    # Is this necessary? If ``field_name`` is ``Variable`` then duplicates are already
    # removed in the initial the step to clean the ARC data dictonary.
    if vertex_data_dictionary["field_name"].duplicated().any():
        raise ValueError("Duplicate field names in the VERTEX dictionary")

    return vertex_data_dictionary
