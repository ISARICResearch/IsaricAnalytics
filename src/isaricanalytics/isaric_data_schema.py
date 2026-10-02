from __future__ import annotations

__all__ = [
    "transform_to_isaric_data_schema",
]


# -- IMPORTS --

# -- Standard libraries --
import pathlib
import typing
import warnings as warnings_

# -- 3rd party libraries --
import adtl
import pandas as pd

# -- Internal ISARIC libraries --
from arc.arc_api import ArcApiClient, ArcApiClientError
from arc.arc_core import get_arc

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
    non_arc_core_columns = set(ids_tables["core"].columns).difference(
        arc_dd["Variable"]
    )
    if non_arc_core_columns:
        _warn_on_non_arc_columns(
            non_arc_core_columns, "core", arc_version, stacklevel=2
        )

    non_arc_long_columns = set(ids_tables["long"].columns).difference(
        arc_dd["Variable"]
    )
    if non_arc_long_columns:
        _warn_on_non_arc_columns(
            non_arc_long_columns, "long", arc_version, stacklevel=2
        )

    if not as_vertex_data:
        return ids_tables

    return {
        "df_map": ids_tables["core"],
        "daily": ids_tables["long"],
        "dictionary": arc_dd,
    }
