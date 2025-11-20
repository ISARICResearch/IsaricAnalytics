#!/usr/bin/env python
"""
core.py: Creates `IsaricData` dataclass.

The `IsaricData` class has methods to:

- Validate the data according to the data schema and the project metadata and data dictionary.
- Describes the data.
- Return views of the data for subsets of subjects and variables.
- Add and remove variables.
"""

__author__ = "Tom Edinburgh"
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
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
    events: Optional[pd.DataFrame]

    def __post_init__(self) -> None:
        """Basic structural validation of required fields."""
        if not isinstance(self.metadata, dict):
            raise TypeError("metadata must be a dictionary")
        for name in ("data_dictionary", "presentation", "outcome"):
            value = getattr(self, name)
            if not isinstance(value, pd.DataFrame):
                raise TypeError(f"{name} must be a pandas DataFrame")

    def validate(self) -> None:
        return

    def describe(self) -> str:
        return

    def get_subject(self, subjid: str, dataframe: str) -> pd.DataFrame:
        return

    def get_variables(self, variables: List[str], dataframe: str) -> pd.DataFrame:
        return

    def get_dtypes(self, dtypes: List[str], dataframe: str) -> pd.DataFrame:
        return

    def add_derived_variable(self, variable: str, dataframe: str, **kwargs) -> pd.DataFrame:
        return

    def add_custom_variable(self, new_variable, dataframe: str, field_name: str, **kwargs) -> pd.DataFrame:
        return

    def remove_variable(self, variable: str, dataframe: str) -> pd.DataFrame:
        return
