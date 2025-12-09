#!/usr/bin/env python
"""
core.py: Creates `IsaricData` dataclass.

The `IsaricData` class has methods to:

- Validate the data according to the data schema and the project metadata and data
  dictionary.
- Describes the data.
- Return views of the data for subsets of subjects and variables.
- Add and remove variables.
"""

__author__ = "Tom Edinburgh"

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pandas as pd


@dataclass
class IsaricData:
    # Required fields
    metadata: Dict[str, Any]
    data_dictionary: pd.DataFrame
    presentation: pd.DataFrame
    outcome: pd.DataFrame

    # Optional fields
    daily: Optional[pd.DataFrame]
    events: Optional[Dict[str, pd.DataFrame]]

    def __post_init__(self) -> None:
        """Validation of all data."""
        self.validate_metadata()
        self.validate_data_dictionary()
        for table_name in ("presentation", "outcome"):
            self.validate_table(table_name)

    def validate_metadata(self) -> None:
        """Validation of metadata.

        Raises:
            TypeError: If metadata is not a dictionary
        """
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")

    def validate_data_dictionary(self) -> None:
        """Validation of data_dictionary.

        Raises:
            TypeError: If data_dictionary is not a pandas DataFrame.
        """
        if not isinstance(self.data_dictionary, pd.DataFrame):
            raise TypeError("data_dictionary must be a pandas DataFrame")

    def validate_table(self, table_name: str) -> None:
        """Validation of a named table.

        Raises:
            TypeError: If the table is not a pandas DataFrame.
        """
        table = getattr(self, table_name)
        if not isinstance(table, pd.DataFrame):
            raise TypeError("%s must be a pandas DataFrame", table_name)

    def describe(self) -> str:
        """Print a summary of the instance. TODO."""
        return

    def get_field_options(self, field_name: str) -> List[Any]:
        """Currently field options stored as a JSON-string inside a pandas dataframe.
        TODO."""
        mask = self.data_dictionary["field_name"] == field_name
        s = self.data_dictionary.loc[mask, "field_options"].item()
        field_options = json.loads(s) if pd.notna(s) and s.strip() else []
        return field_options

    def get_subject(self, subjid: str, table_name: str) -> pd.DataFrame:
        return

    def get_fields(self, field_names: List[str], table_name: str) -> pd.DataFrame:
        return

    def get_type(self, field_type: str, table_name: str) -> pd.DataFrame:
        return

    def add_derived_field(
        self, field_name: str, table_name: str, **kwargs
    ) -> pd.DataFrame:
        return

    def add_custom_field(
        self, new_field_name: str, table_name: str, **kwargs
    ) -> pd.DataFrame:
        return

    def remove_field(self, field_name: str, table_name: str) -> pd.DataFrame:
        return
