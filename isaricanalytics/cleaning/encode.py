#!/usr/bin/env python
"""
encode.py: Functions for encoding data with a wrapper.
- One-hot-encoding categorical fields into separate boolean fields.
- Inverting a one-hot-encoding.
- Converting Yes/No/Unknown fields into booleans (True/False/NaN)
"""

__author__ = "Tom Edinburgh"

from typing import Any, Dict, List, Optional

import pandas as pd

from isaricanalytics.data import IsaricData


def one_hot_encode(
    data: IsaricData,
    table_name: str,
    field_names: List[str],
    collapse_to_other: bool = False,
    collapse_threshold: Optional[float] = None,
) -> IsaricData:
    return


def inverse_one_hot_encode(
    data: IsaricData,
    table_name: str,
    field_names: List[str],
    collapse_to_other: bool = False,
    collapse_threshold: Optional[float] = None,
) -> IsaricData:
    return


def categorical_ynu_to_boolean(
    data: IsaricData,
    table_name: str,
    field_names: List[str],
) -> IsaricData:
    return


METHODS = {
    "one-hot-encode": one_hot_encode,
    "inverse-one-hot-encode": inverse_one_hot_encode,
    "categorical_ynu-to-boolean": categorical_ynu_to_boolean,
}


def encode(
    data: IsaricData,
    method: str,
    table_name: str,
    field_names: List[str],
    **kwargs,
) -> IsaricData:
    return
