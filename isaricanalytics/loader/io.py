#!/usr/bin/env python
"""
io.py: Loader utilities for reading data from file into a `IsaricData` object.

This module defines a `Loader` class to:

- Read project metadata from `metadata.json` file.
- Read a project `data_dictionary` .csv file.
- Load data from .csv files as described in the metadata, enforcing dtypes specified
in the data dictionary.

The top-level function `load_data_from_file` is a convenience wrapper that
creates a `Loader` object, reads the required files into an `IsaricData`
object and runs the validation method of `IsaricData` dataclass.
"""

__author__ = "Tom Edinburgh"

import json
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd

from isaricanalytics.data import IsaricData
from isaricanalytics.logger import setup_logger

logger = setup_logger(__name__)


class Loader:
    """Utility class for loading project metadata, data dictionary and data.

    A `Loader` instance is tied to a directory path which must contain
    `metadata.json` file. The metadata describes the names and filenames of
    data and data dictionary. These are usual in the same directory.

    Args:
        path: Directory that contains project files (at least ``metadata.json``).
        encoding: Default text encoding used when reading JSON and
          CSV files. Defaults to ``"utf-8"``.

    Attributes:
        path: Path object for the specified path
        encoding: As above
        metadata:
          Project metadata, empty on initialisation. Loaded using
          :method:`load_metadata`.
        data_dictionary: Project data_dictionary, empty on initialisation.
          Loaded using :method:`load_data_dictionary`.

    Raises:
        FileNotFoundError: If ``path`` does not exist or is not a directory.
    """

    def __init__(self, path: str, encoding: str = "utf-8") -> None:
        if not isinstance(path, str):
            raise TypeError("path must be string-valued")
        if not isinstance(encoding, str):
            raise TypeError("encoding must be string-valued")
        self.path = Path(path)
        self.encoding = encoding

        if not self.path.is_dir():
            raise FileNotFoundError(self.path)

        self.metadata: Optional[Dict[str, Any]] = None
        self.data_dictionary: Optional[pd.DataFrame] = None
        logger.info("Set project path to %s", path)

    def load_metadata(self) -> Dict[str, Any]:
        """Load and parse ``metadata.json``.

        Returns:
            A dict of the parsed ``metadata.json``.

        Raises:
            FileNotFoundError: If the metadata file does not exist in the directory.
        """
        metadata_path = self.path / "metadata.json"

        if not metadata_path.exists():
            raise FileNotFoundError(metadata_path)

        with open(metadata_path, "r", encoding=self.encoding) as json_data:
            self.metadata = json.load(json_data)
            logger.info("Loaded project metadata.")

        # Get path specified in metadata, must match path specified on init if present
        path_from_metadata = self.metadata.get("path", None)
        if (
            path_from_metadata
            and Path(path_from_metadata).resolve() != self.path.resolve()
        ):
            raise ValueError("metadata field `path` must equal :attr:`path`")
        return self.metadata

    def load_data_dictionary(self) -> pd.DataFrame:
        """Load the project data dictionary.

        Returns:
            Data dictionary as a pandas.DataFrame.

        Raises:
            ValueError: If metadata is missing.
            TypeError:
              If relevant metadata keys are not string-valued: 'path',
              'files.data_dictionary.filename', 'files.data_dictionary.encoding'
            FileNotFoundError: If data dictionary file is not found.
        """

        if self.metadata is None:
            raise ValueError(
                "metadata must be loaded first (using :method:`load_metadata`)"
            )

        filename = (
            self.metadata.get("files", {})
            .get("data_dictionary", {})
            .get("filename", "data_dictionary.csv")
        )
        if not isinstance(filename, str):
            raise TypeError(
                "metadata key 'files.data_dictionary.filename' must be string-valued "
                "if it exists"
            )

        encoding = (
            self.metadata.get("files", {})
            .get("data_dictionary", {})
            .get("encoding", self.encoding)
        )
        if not isinstance(encoding, str):
            raise TypeError(
                "metadata key 'files.data_dictionary.encoding' must be string-valued "
                "if it exists"
            )

        data_dictionary_path = self.path / filename
        if not data_dictionary_path.exists():
            raise FileNotFoundError(data_dictionary_path)

        data_dictionary = pd.read_csv(
            data_dictionary_path,
            dtype=str,
            encoding=encoding,
        )

        self.data_dictionary = data_dictionary

        # TODO: validate data_dictionary?
        logger.info("Loaded project data_dictionary.")
        return self.data_dictionary

    def load_df(self, name: str) -> pd.DataFrame:
        """Load a dataframe using project metadata and data dictionary.

        Both metadata and data dictionary must be loaded before. The data dictionary
        should provide dtypes of the data. Text/categorical variables are treated as
        strings when the file is read. Datetime columns are converted to dtype
        datetime64[ns] after reading.

        Args:
            name: name of the dataframe to load (must be present in
              ``metadata['files']``).

        Returns:
            The loaded pandas.DataFrame.

        Raises:
            ValueError: If metadata or data_dictionary is missing.
            TypeError:
              If relevant metadata keys are not string-valued e.g. 'path'
              'files.data_dictionary.filename', 'files.data_dictionary.encoding'
            FileNotFoundError: If data file is not found.
        """

        if self.metadata is None:
            raise ValueError(
                "metadata must be loaded first (using :method:`load_metadata`)"
            )

        if self.data_dictionary is None:
            raise ValueError(
                "data dictionary must be loaded first "
                "(using :method:`load_data_dictionary`)"
            )

        file_metadata = self.metadata.get("files", {}).get(name, {})
        # If an events dataframe, then need to go one level deeper in the metadata
        if not file_metadata:
            file_metadata = (
                self.metadata.get("files", {}).get("events", {}).get(name, {})
            )

        if not file_metadata:
            logger.warning(
                "dataframe %s is not listed as a file in metadata.json "
                "or has no metadata",
                name,
            )
            return

        filename = file_metadata.get("filename", f"{name}.csv")
        if not isinstance(filename, str):
            raise TypeError(
                "metadata key 'files.%s.filename' must be string-valued if it exists",
                name,
            )

        encoding = file_metadata.get("encoding", self.encoding)
        if not isinstance(encoding, str):
            raise TypeError(
                "metadata key 'files.%s.encoding' must be string-valued if it exists",
                name,
            )

        data_path = self.path / filename
        if not data_path.exists():
            raise FileNotFoundError(data_path)

        str_mask = (self.data_dictionary["table_name"] == name) & (
            self.data_dictionary["field_type"].isin(["freetext", "categorical"])
        )
        str_variables = self.data_dictionary.loc[str_mask, "field_name"].tolist()
        dtype_dict = {x: str for x in str_variables}
        na_values = {x: "" for x in str_variables}

        df = pd.read_csv(
            data_path,
            dtype=dtype_dict,
            keep_default_na=False,
            na_values=na_values,
            encoding=encoding,
        )

        # Convert datetime variables
        date_mask = (self.data_dictionary["table_name"] == name) & (
            self.data_dictionary["field_type"] == "datetime"
        )
        date_variables = self.data_dictionary.loc[date_mask, "field_name"].tolist()
        df[date_variables] = df[date_variables].apply(
            lambda x: pd.to_datetime(x, errors="coerce")
        )

        logger.info("Loaded project dataframe: %s.", name)
        return df


def load_data_from_file(path: str, validate: bool = True) -> IsaricData:
    """Wrapper function to load project data into `IsaricData` instance
    and validates this using the validate method of the `IsaricData` class.

    Args:
        path: Path to the project directory.

    Returns:
        A populated :class:`IsaricData` instance.

    Examples:
        >>> from isaricanalytics.loader import load_data_from_file
        >>> data = load_data_from_file("examples/datasets/h5nx_synthetic")
        >>> data.presentation.head()
    """
    loader = Loader(path=path)
    metadata = loader.load_metadata()
    data_dictionary = loader.load_data_dictionary()

    presentation = loader.load_df(name="presentation")
    outcome = loader.load_df(name="outcome")
    daily = loader.load_df(name="daily")  # may return None if not present in metadata

    events_metadata = metadata.get("files", {}).get("events", {})
    if events_metadata:  # i.e. a non-empty dict
        events = {name: loader.load_df(name=name) for name in events_metadata.keys()}

    data = IsaricData(
        metadata=metadata,
        data_dictionary=data_dictionary,
        presentation=presentation,
        outcome=outcome,
        daily=daily,
        events=events if events_metadata else None,
    )
    return data
