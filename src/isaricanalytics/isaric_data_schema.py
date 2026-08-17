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
import isaricanalytics.isaric_transformations as tf


def transform_to_isaric_data_schema(
    parser_file: str | pathlib.Path, data_file: str | pathlib.Path
) -> dict[str, pd.DataFrame]:
    """:py:class:`dict` : A dict of ISARIC schema-compliant short- (core) and long-format datasets as Pandas dataframes.

    Parameters
    ----------
    parser_file : str or pathlib.Path
        The parser TOML file path.

    data_file : str or pathlib.Path
        The data file path.

    Returns
    -------
    dict
        A dict of two Pandas dataframes representing short- and long-format
        ISARIC schema-compliant transforms of the original dataset.
    """  # noqa : E501
    return adtl.parse(parser_file, data_file, include_transform=tf.__file__)
