#!/usr/bin/env python
"""
filters.py: Functions for filtering tables in a IsaricData object.
"""

import pandas as pd

from isaricanalytics.data import IsaricData
from isaricanalytics.logger import setup_logger

logger = setup_logger(__name__)


def skip_logic_filter(
    data: IsaricData,
    field_name: str,
) -> pd.Series:
    """Create a mask identifying where the skip logic for the specified field is met.
    TODO: handle the skip logic.

    Args:
        data: An IsaricData instance.
        field_name: Field name identifying the field that contains skip logic.

    Returns:
        A boolean mask for the field as a pandas Series.
    """
    data_dictionary = data.data_dictionary

    if field_name not in data_dictionary["field_name"].values:
        raise ValueError(
            f"field_name {field_name} does not exist in the data dictionary"
        )

    idx = data_dictionary.index[
        data_dictionary["field_name"] == field_name
    ].tolist()[0]

    table_name = data_dictionary.loc[idx, "table_name"]
    df = getattr(data, table_name)
    field = df[field_name]

    # TODO: handle the skip logic rather than just returning True
    mask = field.apply(lambda x: True)
    logger.debug("Filter for skip logic is not completed, returns a True valued mask")
    return mask
