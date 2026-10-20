from __future__ import annotations

__all__ = [
    "get_vertex_df_forms_proxy",
    "get_vertex_df_map_proxy",
    "get_parser_source_field_map",
    "get_parser_toml_map",
    "IsaricDataSchemaTransformationException",
    "transform_to_isaric_data_schema",
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
from arc.arc_api import ArcApiClient, ArcApiClientError
from arc.arc_core import get_arc

# -- Internal ISARIC libraries --
import isaricanalytics.isaric_transformations as tf


class IsaricDataSchemaTransformationException(Exception): ...


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
    arc_version: str | None = None,
    /,
    *,
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
        associated with the ARC version; defaults to ``None``.

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
        A dict which could be in one of two forms:
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
    # columns in the parser file.
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
        "df_forms_dict": get_vertex_df_forms_proxy(core_table, long_table),
        "dictionary": arc_dd,
        "quality_report": {},
    }


def get_vertex_df_map_proxy(
    ids_core_table: pd.DataFrame, ids_long_table: pd.DataFrame, /
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns a proxy for the VERTEX ``df_map`` containing one-row-per-patient data from an inner merge of the ISARIC data schema core and long tables on patient ID.

    Parameters
    ----------
    ids_core_table : pandas.DataFrame
        The ISARIC data schema core table.

    ids_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    Returns
    -------
    pandas.DataFrame
        A single dataframe with only one row per patient, combining columns
        from both the core table and long table, and converting multi-valued
        columns in the merged table to list-valued columns.
    """  # noqa : E501
    coretb = ids_core_table.drop(
        columns=[col for col in ids_core_table.columns if col.startswith("adtl")]
    )
    longtb = ids_long_table.drop(
        columns=[col for col in ids_long_table.columns if col.startswith("adtl")]
    )

    # Inner-merge the core and long tables on patient ID (``subjid``) and keep
    # core table columns without suffixes.
    merged = coretb.merge(longtb, on=["subjid"], how="inner", suffixes=(None, "_y"))

    # Drop any columns with ``"_y"`` suffixes (from the long table) because
    # there must be unsuffixed versions of these from the core table from the
    # merge above.
    merged.drop(
        columns=[col for col in merged.columns if col.endswith("_y")], inplace=True
    )

    # An intermediate step to convert all non-patient ID columns to list-valued
    # columns.
    non_patient_id_cols = merged.columns.difference(["subjid"]).tolist()
    merged = merged.groupby(["subjid"]).agg(
        {col: lambda values: values.tolist() for col in non_patient_id_cols}
    )

    # Identify and drop any non-patient ID column with more than one (unique)
    # value per patient.
    multivalued_cols = [
        col
        for col in non_patient_id_cols
        if all(len(set(v)) > 1 for v in merged[col].values)
    ]
    merged.drop(columns=multivalued_cols, inplace=True)

    return merged.explode(
        merged.columns.difference(["subjid"]).tolist()
    ).drop_duplicates()


def get_vertex_df_forms_proxy(
    ids_core_table: pd.DataFrame, ids_long_table: pd.DataFrame, /
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : Returns a proxy for the VERTEX ``df_forms`` dict containing a dataframe of patient interaction data for each patient interaction phase/state.

    Parameters
    ----------
    ids_core_table : pandas.DataFrame
        The ISARIC data schema core table.

    ids_long_table : pandas.DataFrame
        The ISARIC data schema long table.

    Returns
    -------
    pandas.DataFrame
        A single dataframe with only one row per patient, combining columns
        from both the core table and long table, and converting multi-valued
        columns in the merged table to list-valued columns.
    """  # noqa : E501
    longtb = ids_long_table.drop(
        columns=[
            col for col in ids_long_table.columns if col.lower().startswith("adtl")
        ]
    )

    # Build the ``df_forms_dict`` proxy using the merged dataframe (``daily``),
    # and the dataframes obtained by grouping the merged dataframe by patient
    # interaction phase (``phase`` column).
    return {
        phase[0]: phase_data.reset_index(drop=True)
        for phase, phase_data in longtb.groupby(["phase"])
    }
