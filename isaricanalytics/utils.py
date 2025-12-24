#!/usr/bin/env python
"""
utils.py: General helper functions.
"""

import re

import pandas as pd


def sanitise_string(string: str) -> str:
    """Replaces uppercase with lowercase, spaces with underscores and then removes
    all characters except lowercase  alphanumeric and underscores.

    Args:
        string: any string

    Returns:
        Modified string.
    """
    s = str(string).strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^0-9a-z_]", "", s)
    return s


def sanitise_field(field: pd.Series) -> pd.Series:
    """Sanitises multiple strings in a field simultaneously.

    Args:
        field: a string-valued pandas Series.

    Returns:
        A modified field with sanitised values
        A dict of the sanitised and original values (as key-value pairs in that order).
    """
    mapping_df = pd.DataFrame.from_dict(
        {value: sanitise_string(value) for value in field},
        orient="index",
        columns=["clean"],
    ).reset_index()

    # Make sure sanitised strings are unique by adding an incremental suffix
    mapping_df["clean"] = mapping_df["clean"].str.cat(
        mapping_df.groupby("clean").cumcount().astype(str),
        sep="__",
    )
    # Only need to append a suffix to repeating sanitised strings
    mapping_df["clean"] = mapping_df["clean"].apply(lambda x: re.sub("\\__0", "", x))

    mapping = mapping_df.set_index("index").to_dict()["clean"]
    sanitised_field = field.replace(mapping)

    return sanitised_field, mapping
