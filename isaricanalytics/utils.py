__all__ = [
    "clean_figure_table",
    "strip_html",
    "strip_nonstandard_unicode_chars",
]

# -- IMPORTS --

# -- Standard libraries --
import re
import typing

# -- 3rd party libraries --
import pandas as pd

# -- Internal libraries --


def strip_html(value: typing.Any) -> str | typing.Any:
    """:py:class:`typing.Any` : Strip HTML elements from a value.

    Parameters
    ----------
    value : typing.Any
        A value.

    Returns
    -------
    str, typing.Any
        Either a string stripped of all HTML elements, or the original non-
        string value.
    """
    if isinstance(value, str):
        return re.sub(r"<.*?>", "", value)

    return value


def strip_nonstandard_unicode_chars(value: typing.Any) -> str | typing.Any:
    """:py:class:`typing.Any` : Strip non-standard Unicode characters from a value.

    The non-standard Unicode characters of interest are defined within the
    function itself, and are currently limited to the "↳" (U+21B3) character,
    but may be extended to include other characters.

    Parameters
    ----------
    value : typing.Any
        A value.

    Returns
    -------
    str, typing.Any
        Either a string stripped of all non-standard Unicode characters, or the
        original non- string value.
    """
    nonstandard_unicode_chars = "↳"

    if isinstance(value, str):
        return re.sub(rf"[{nonstandard_unicode_chars}]", "", value)

    return value


def clean_figure_table(figure_table: pd.DataFrame) -> pd.DataFrame:
    """:py:class:pandas.DataFrame : A cleaned figure table dataframe.

    The cleaning steps are unique to the Plotly graph object table format from
    which the table CSVs were originally, which contain HTML styling elements
    and non-standard (non-alphabetic) Unicode characters. The cleaning is the
    removal of such characters.

    Parameters
    ----------
    figure_table : pandas.DataFrame
        The original figure table as a Pandas dataframe.

    Returns
    -------
    pandas.DataFrame
        The cleaned figure table.
    """
    # The use of `pandas.DataFrame.map` here is not absolutely optimal, as
    # `map` applies changes across the dataframe element-wise, but is the
    # safer choice given that the dataframe may contain a number of non-string
    # columns which cannot be known in advance, while the cleaning steps
    # currently only apply to string values.
    return figure_table.map(strip_html).map(strip_nonstandard_unicode_chars)
