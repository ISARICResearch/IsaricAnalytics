from __future__ import annotations

__all__ = [
    "get_vertex_df_forms_proxy",
    "get_vertex_df_map_proxy",
    "get_parser_source_field_map",
    "get_parser_toml_map",
    "IsaricDataSchemaTransformationException",
    "transform_to_isaric_data_schema",
    "transform_to_vertex",
]


# -- IMPORTS --

# -- Standard libraries --
import pathlib
import tomllib
import typing
import warnings as warnings_
from itertools import chain, product

# -- 3rd party libraries --
import adtl
import pandas as pd

# -- Internal ISARIC libraries --
from arc.arc_api import ArcApiClient, ArcApiClientError
from arc.arc_core import get_arc

import isaricanalytics.isaric_transformations as tf


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
                "daily": <patient observations dataframe>,
                "dictionary": <ARC data dictionary>
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
                "daily": <patient observations dataframe>,
                "dictionary": <ARC data dictionary>
            }
    Raises
    ------
    IsaricDataSchemaTransformationException
        In case of an ARC API client exception.
    """  # noqa : E501
    # Call ADTL to parse the data and retrieve the core and long-format tables.
    ids_tables = adtl.parse(parser_file, data_file, include_transform=tf.__file__)
    core_table = ids_tables["core"]
    long_table = ids_tables["long"]

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
    non_arc_core_columns = set(core_table.columns).difference(arc_dd["Variable"])
    if non_arc_core_columns:
        _warn_on_non_arc_columns(
            non_arc_core_columns, "core", arc_version, stacklevel=2
        )

    non_arc_long_columns = set(long_table.columns).difference(arc_dd["Variable"])
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

    return {
        "df_map": get_vertex_df_map_proxy(core_table, long_table),
        "df_forms_dict": get_vertex_df_forms_proxy(long_table),
        "dictionary": arc_dd,
        "quality_report": {},
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
    """
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

    df_map, vertex_dictionary = get_vertex_df_map_proxy(
        isaric_core_table,
        isaric_long_table,
        arc_dd,
    )
    return {
        "df_map": df_map,
        "df_forms_dict": get_vertex_df_forms_proxy(isaric_long_table),
        "dictionary": vertex_dictionary,
        "quality_report": {},
    }


def get_vertex_df_map_proxy(
    isaric_core_table: pd.DataFrame,
    isaric_long_table: pd.DataFrame,
    arc_dd: pd.DataFrame,
    /,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """:py:class:`pandas.DataFrame` : Returns a proxy for the VERTEX ``df_map`` containing one-row-per-patient data from an inner merge of the ISARIC data schema core and long tables on patient ID.

    Parameters
    ----------
    isaric_core_table : pandas.DataFrame
        The ISARIC data schema core table.

    isaric_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    Returns
    -------
    pandas.DataFrame
        A single dataframe with only one row per patient.
    """  # noqa : E501
    coretb = isaric_core_table.drop(
        columns=[col for col in isaric_core_table.columns if col.startswith("adtl")]
    )
    longtb = isaric_long_table.drop(
        columns=[col for col in isaric_long_table.columns if col.startswith("adtl")]
    )

    # Retain one copy of each identical observation.
    longtb = longtb.drop_duplicates()

    # Count observations per patient and attribute.
    counts = longtb.groupby(
        ["dataset_id", "subjid", "attribute"],
        dropna=False,
    ).size()

    # An attribute qualifies only if no patient has multiple observations.
    maximum_count = counts.groupby(level="attribute").max()
    eligible_attributes_dfmap = maximum_count[maximum_count <= 1].index

    # subset the long table to only those attributes that are eligible for
    # inclusion in the df_map (happening exactly once per patient in the
    # observation period
    single_observation_long = longtb.loc[
        longtb["attribute"].isin(eligible_attributes_dfmap)
    ].copy()

    ##

    observations = single_observation_long.copy()

    # Ensure optional columns exist and convert blank cells to missing.
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

    patient_keys = ["dataset_id", "subjid"]

    wide = observations.pivot(
        index=patient_keys,
        columns=["attribute", "_unit"],
        values="_value",
    )

    # Convert attribute/unit pairs into simple column names.
    wide.columns = [
        f"{attribute}_{unit}" if unit else attribute for attribute, unit in wide.columns
    ]

    wide.columns.name = None
    # Create independent attribute_duration columns.
    duration_rows = observations.loc[observations["_duration"].notna()]

    if not duration_rows.empty:
        wide_duration = duration_rows.pivot(
            index=patient_keys,
            columns="attribute",
            values="_duration",
        )

        wide_duration.columns = [
            f"{attribute}_duration" for attribute in wide_duration.columns
        ]

        wide = pd.concat([wide, wide_duration], axis=1)

    # Prevent ambiguous or overlapping column names.
    if not wide.columns.is_unique:
        raise ValueError("Generated df_map column names are not unique")

    overlaps = sorted(set(wide.columns).intersection(coretb.columns))
    if overlaps:
        raise ValueError(f"Generated columns overlap core fields: {overlaps}")

    wide.columns.name = None

    # Convert patient identifiers from the index into columns,
    # then attach the observations to every core record.
    df_map = coretb.merge(
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

    # Build a dictionary for df_map, keeping ARC's original form groups.
    arc = arc_dd.fillna("").set_index("Variable")

    if not arc.index.is_unique:
        raise ValueError("ARC contains duplicate Variable names")

    # Match generated columns to their original ARC attributes.
    field_sources = {column: (column, "", False) for column in df_map.columns}

    for attribute, unit in (
        observations[["attribute", "_unit"]]
        .drop_duplicates()
        .itertuples(index=False, name=None)
    ):
        column = f"{attribute}_{unit}" if unit else attribute

        if column in df_map.columns:
            field_sources[column] = (attribute, unit, False)

    for attribute in duration_rows["attribute"].drop_duplicates():
        column = f"{attribute}_duration"

        if column in df_map.columns:
            field_sources[column] = (attribute, "", True)

    # Metadata for schema/derived fields without a direct ARC definition.

    extra_metadata = {
        "dataset_id": (
            "presentation",
            "freetext",
            "Dataset identifier",
            "study",
            "STUDY",
        ),
        "dataset_disease": (
            "presentation",
            "categorical",
            "Dataset disease",
            "study",
            "STUDY",
        ),
        "siteid": (
            "presentation",
            "freetext",
            "Site identifier",
            "study",
            "STUDY",
        ),
        "site": (
            "presentation",
            "categorical",
            "Site",
            "study",
            "STUDY",
        ),
        "demog_country_iso3": (
            "presentation",
            "categorical",
            "Country ISO3 code",
            "demog",
            "DEMOGRAPHICS",
        ),
        "country_iso": (
            "presentation",
            "categorical",
            "Country ISO Code",
            "country",
            "COUNTRY",
        ),
        "demog_age_days": (
            "presentation",
            "numeric",
            "Age (days)",
            "demog",
            "DEMOGRAPHICS",
        ),
        "outco_binary_outcome": (
            "outcome",
            "categorical",
            "Outcome (binary)",
            "outco",
            "OUTCOME",
        ),
    }

    type_map = {
        "number": "numeric",
        "calc": "numeric",
        "slider": "numeric",
        "text": "freetext",
        "notes": "freetext",
        "descriptive": "freetext",
        "date_dmy": "date",
        "datetime_dmy": "date",
        "radio": "categorical",
        "dropdown": "categorical",
        "user_list": "categorical",
        "list": "categorical",
        "yesno": "binary",
        "truefalse": "binary",
    }

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
        source, unit, is_duration = field_sources[column]

        if column in extra_metadata:
            (
                form,
                field_type,
                label,
                parent,
                section_label,
            ) = extra_metadata[column]

        elif source in arc.index:
            metadata = arc.loc[source]

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

    vertex_dictionary = pd.DataFrame(
        list(sections.values()) + rows,
        columns=dictionary_columns,
    )

    if vertex_dictionary["field_name"].duplicated().any():
        raise ValueError("Duplicate field names in the VERTEX dictionary")

    return df_map, vertex_dictionary


def get_vertex_df_forms_proxy(isaric_long_table: pd.DataFrame, /) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns a proxy for the VERTEX ``df_forms`` dict containing a dataframe of patient interaction data for each patient interaction phase/state.

    Parameters
    ----------
    isaric_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    Returns
    -------
    pandas.DataFrame
        A single dataframe with one or more rows per patient.
    """  # noqa : E501
    longtb = isaric_long_table.drop(
        columns=[
            col for col in isaric_long_table.columns if col.lower().startswith("adtl")
        ]
    )

    # Build the ``df_forms_dict`` proxy using the merged dataframe (``daily``),
    # and the dataframes obtained by grouping the merged dataframe by patient
    # interaction phase (``phase`` column).
    return {
        phase[0]: phase_data.reset_index(drop=True)
        for phase, phase_data in longtb.groupby(["phase"])
    }
