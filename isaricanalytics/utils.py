from __future__ import annotations

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
import pandas

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

    Examples
    --------
    >>> strip_html("<b><i>A value</i></b>")
    'A value'
    >>> strip_html("<p>This is a paragraph.</p>")
    'This is a paragraph.'
    """  # noqa : E501
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

    Examples
    --------
    >>> strip_nonstandard_unicode_chars("A value with a special Unicode ↳ character")
    'A value with a special Unicode  character'
    >>> strip_nonstandard_unicode_chars("<p>This is a paragraph ending with a special Unicode character ↳.</p>")
    '<p>This is a paragraph ending with a special Unicode character .</p>'
    """  # noqa : E501
    nonstandard_unicode_chars = "↳"

    if isinstance(value, str):
        return re.sub(rf"[{nonstandard_unicode_chars}]", "", value)

    return value


def clean_figure_table(figure_table: pandas.DataFrame) -> pandas.DataFrame:
    """:py:class:`pandas.DataFrame` : A cleaned figure table dataframe.

    This function is not intended to be highly generic, but was written with
    the aim of producing clean dataframes for the plotting functions in the
    :py:mod:`isaricanalytics.visualisation` library. The cleaning steps are:

    * removal of HTML styling elements
    * removal of non-standard (non-alphabetic) Unicode characters, currently
      limited to ``↳``.

    Parameters
    ----------
    figure_table : pandas.DataFrame
        The original figure table as a Pandas dataframe.

    Returns
    -------
    pandas.DataFrame
        The cleaned figure table.

    Examples
    --------
    >>> import io, pandas as pd
    >>> pd.set_option("display.max_columns", None)
    >>> data = pd.read_csv(io.StringIO(
    ...     '''
    ...     Variable,All,Discharged,Death,Censored
    ...     <b>Totals</b>,1000,219,326,455
    ...     <b><i>COMPLICATIONS</i></b>,,,,
    ...     <b>Seizure</b> (*),665 (81.7) | 814,148 (80.9) | 183,207 (79.6) | 260,310 (83.6) | 371
    ...     <b>Focal neurological signs</b> (*),702 (74.8) | 938,156 (75.4) | 207,231 (75.5) | 306,315 (74.1) | 425
    ...     <b>Encephalitis</b> (*),481 (52.6) | 914,102 (52.0) | 196,161 (53.5) | 301,218 (52.3) | 417
    ...     <b>Meningitis</b> (*),781 (90.2) | 866,173 (88.7) | 195,252 (91.0) | 277,356 (90.4) | 394
    ...     <b>Cardiac arrhythmia</b> (*),241 (26.7) | 901,64 (32.0) | 200,70 (24.1) | 291,107 (26.1) | 410
    ...     '''
    ... ), skipinitialspace=True)
    >>> cleaned_data = clean_figure_table(data)
    >>> cleaned_data
                           Variable               All        Discharged             Death          Censored
    0                        Totals              1000               219               326               455
    1                 COMPLICATIONS               NaN               NaN               NaN               NaN
    2                   Seizure (*)  665 (81.7) | 814  148 (80.9) | 183  207 (79.6) | 260  310 (83.6) | 371
    3  Focal neurological signs (*)  702 (74.8) | 938  156 (75.4) | 207  231 (75.5) | 306  315 (74.1) | 425
    4              Encephalitis (*)  481 (52.6) | 914  102 (52.0) | 196  161 (53.5) | 301  218 (52.3) | 417
    5                Meningitis (*)  781 (90.2) | 866  173 (88.7) | 195  252 (91.0) | 277  356 (90.4) | 394
    6        Cardiac arrhythmia (*)  241 (26.7) | 901   64 (32.0) | 200   70 (24.1) | 291  107 (26.1) | 410
    """  # noqa : E501
    return figure_table.map(strip_html).map(strip_nonstandard_unicode_chars)


if __name__ == "__main__":  # pragma: no cover
    # Doctest the module from the project root using
    #
    #     PYTHONPATH="isaricanalytics" python3 -m doctest -v isaricanalytics/utils.py  # noqa : E501
    #
    import doctest

    doctest.testmod()
