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

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from copy import deepcopy
import pandas as pd

from isaricanalytics.utils import sanitise_string


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
        self.validate()

    def validate(self) -> None:
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

        field_name_check = self.data_dictionary['field_name'].apply(
            lambda x: x != sanitise_string(x) or not str(x)[0].isalpha()
        )
        if field_name_check.any():
            field_names = ", ".join(
                self.data_dictionary.loc[field_name_check, 'field_name']
            )
            raise ValueError(f"field_names ({field_names}) don't conform to schema")

    def validate_table(self, table_name: str) -> None:
        """Validation of a named table.

        Raises:
            TypeError: If the table is not a pandas DataFrame.
        """
        table = getattr(self, table_name)
        if not isinstance(table, pd.DataFrame):
            raise TypeError(f"{table_name} must be a pandas DataFrame")

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

    def get_field_names(self, field_types: List[str], table_names: List[str]) -> List[str]:
        """Get field names by field types and/or table names. TODO properly"""
        mask = (
            self.data_dictionary["field_type"].isin(field_types)
            & self.data_dictionary["table_name"].isin(table_names)
        )
        return self.data_dictionary.loc[mask, "field_name"].tolist()

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

    def copy(self, table_names: Optional[List[str]] = None) -> "IsaricData":
        """
        Return a deep copy of this IsaricData instance.

        Args:
            table_names:
                Optional list of attribute names that correspond to pandas DataFrames.
                If None, deep copy all attributes that are pandas DataFrames.

        Returns:
            A new IsaricData instance with copied attributes.
        """
        # create a new empty instance, avoid re-running __init__
        new = self.__class__.__new__(self.__class__)

        for name, value in self.__dict__.items():
            if (
                isinstance(value, pd.DataFrame)
                and table_names is None or name in table_names
            ):
                new.__dict__[name] = value.copy(deep=True)

            elif isinstance(value, dict):
                new.__dict__[name] = deepcopy(value)

            else:
                new.__dict__[name] = value

        return new
