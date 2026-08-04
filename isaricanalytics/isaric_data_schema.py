from __future__ import annotations

__all__ = [
    "transform_to_isaric_data_schema",
]


# -- IMPORTS --

# -- Standard libraries --
import pathlib

# -- 3rd party libraries --
import adtl
import pandas as pd

# -- Internal libraries --


def transform_to_isaric_data_schema(
    parser_file: str | pathlib.Path, data_file: str | pathlib.Path
) -> pd.DataFrame:
    """:py:class:`pandas.DataFrame` : An ISARIC schema-compliant dataset as a Pandas dataframe.

    Parameters
    ----------
    parser_file : str or pathlib.Path
        The parser TOML file path.

    data_file : str or pathlib.Path
        The data file path.

    Returns
    -------
    pandas.DataFrame
        An ISARIC schema-compliant dataset as a Pandas dataframe.
    """  # noqa : E501
    return adtl.parse(pathlib.Path(parser_file), pathlib.Path(data_file))
