#!/usr/bin/env python
"""
encode.py: Functions for encoding data with a wrapper.
- One-hot-encoding categorical fields into separate boolean fields.
- Inverting a one-hot-encoding.
- Converting Yes/No/Unknown fields into booleans (True/False/NaN)
"""

from typing import List, Optional, Dict, Callable
import inspect

import pandas as pd
import numpy as np

from isaricanalytics.data import IsaricData
from isaricanalytics.logger import setup_logger
from isaricanalytics.utils import sanitise_field
from isaricanalytics.cleaning import filters

logger = setup_logger(__name__)


class Encoder():
    def __init__(self, data: IsaricData, validate: bool = True, inplace: bool = False):
        """Init for data instance and arguments passed to methods.

        Args:
            data: An IsaricData instance.
            validate:
                Performs the validation checks for IsaricData instance when True.
            inplace:
                If False, creates a deep copy of the IsaricData instance. If True, will
                mutate the existing IsaricData instance.
        """
        self.data = data
        self.validate = validate
        self.inplace = inplace

    def _collapse_options(
        self,
        field: pd.Series,
        cumulative_threshold: Optional[float] = None,
        max_n_options: Optional[int] = None,
        replacement_string: str = "other",
    ) -> pd.Series:
        """Combine several field option values into a single replacement value,
        based on their frequency.

        Args:
            field: A pandas Series. Should be string-valued.
            cumulative_threshold:
                Threshold for collapsing values into :replacement_string:.
                Must be between 0 and 1. A value of 0.8 means that the most
                frequent categories up to a cumulative proportion of 0.8 (inclusive of
                NaN values) are retained and all else are replaced with
                :replacement_string:.
            max_n_options:
                Threshold for collapsing values into :replacement_string:.
                A value of `n` means that the `n` most frequent categories are
                retained and all else are replaced with :replacement_string:.
            replacement_string:
                String value to replace infrequent values within the field.

        Returns:
            The modified pandas Series.
        """
        invalid_threshold = cumulative_threshold < 0 or cumulative_threshold > 1
        if cumulative_threshold and invalid_threshold:
            logger.debug(":cumulative_threshold: invalid, ignoring :collapse_options:")
            return field

        field = field.astype(object)

        nan_string = "missing"
        counts = field.fillna(nan_string).value_counts(normalize=True)

        if cumulative_threshold:
            # Shift before cumsum to include the field option that takes it over
            # the threshold
            condition = counts.shift().fillna(0).cumsum() > cumulative_threshold
            replace_values = counts[condition].index.tolist()
            field.loc[field.isin(replace_values)] = replacement_string

        if max_n_options:
            replace_values = counts.index[max_n_options + 1:].tolist()
            field.loc[field.isin(replace_values)] = replacement_string

        return field

    def one_hot_encode(
        self,
        table_name: str,
        field_names: Optional[List[str]] = None,
        collapse_to_other: bool = False,
        cumulative_threshold: Optional[float] = None,
        max_n_options: Optional[int] = None,
    ) -> IsaricData:
        """One-hot-encode fields in a single table (and updates data dictionary).

        Args:
            table_name: Name of the table to be updated.
            field_names:
                List of field names to be one-hot-encoded. Only categorical fields will
                actually be one-hot-encoded. If None, all categorical fields in the
                table will be one-hot-encoded.
            collapse_to_other:
                Indicator for collapsing values into "Other" before OHE. Note: this may
                mean that the OHE is irreversible! Ignored if `cumulative_threshold` and
                `max_n_options` are both None. If True and both are specified, they will
                both be applied independently.
            cumulative_threshold:
                Threshold for collapsing values into "Other".  Must be between 0 and 1.
                Ignored if `collapse_to_other` is False. A value of 0.8 means that the most
                frequent categories up to a cumulative proportion of 0.8 (inclusive of NaN
                values) are retained and all else are converted to "Other" before OHE.
            max_n_options:
                Threshold for collapsing values into "Other". Ignored if
                `collapse_to_other` is False. A value of `n` means that the `n` most
                frequent categories are retained and all else are converted to "Other"
                before OHE.

        Returns:
            The modified IsaricData instance.
        """

        if not hasattr(self.data, table_name):
            logger.info(
                "%s is not a table in %s, one-hot-encoding not completed",
                table_name,
                self.data
            )
            return self.data

        if not self.inplace:
            self.data = self.data.copy(table_names=[table_name, "data_dictionary"])

        df = getattr(self.data, table_name)
        data_dictionary = self.data.data_dictionary

        categorical_field_names = self.data.get_field_names(
            field_types=["categorical"],
            table_names=[table_name],
        )
        if not field_names:
            field_names = categorical_field_names

        valid_field_names = [
            name for name in field_names if name in categorical_field_names
        ]

        if collapse_to_other and (cumulative_threshold or max_n_options):
            for field_name in valid_field_names:
                # TODO: skip_logic_filter function is incomplete
                # Keep rows where skip logic is satisfied
                mask = filters.skip_logic_filter(
                    data=self.data,
                    field_name=field_name,
                )
                df.loc[mask, field_name] = self._collapse_options(
                    field=df.loc[mask, field_name],
                    cumulative_threshold=cumulative_threshold,
                    max_n_options=max_n_options,
                    replacement_string="other"
                )

        field_option_mapping = {}
        field_nan_mask = {}
        for field_name in valid_field_names:
            nan_mask = df[field_name].isna()
            # mapping is a dict containing "cleaned" field options
            df.loc[~nan_mask, field_name], mapping = (
                sanitise_field(df.loc[~nan_mask, field_name])
            )
            field_option_mapping[field_name] = mapping
            field_nan_mask[field_name] = df[field_name].isna()

        df = pd.get_dummies(
            data=df,
            columns=valid_field_names,
            prefix_sep="___",
            dummy_na=False
        )

        data_dictionary_inserts = {}
        for field_name in valid_field_names:
            nan_mask = field_nan_mask[field_name]
            mapping = field_option_mapping[field_name]
            ohe_field_names = [
                f"{field_name}___{clean_option}" for clean_option in mapping.values()
            ]

            if any(ohe_field_name not in df.columns for ohe_field_name in ohe_field_names):
                raise KeyError("Expected OHE field does not exist")

            df[ohe_field_names] = df[ohe_field_names].astype(object)
            df.loc[nan_mask, ohe_field_names] = np.nan

            # Add one-hot-encoded fields to the data dictionary
            idx = data_dictionary.index[
                data_dictionary["field_name"] == field_name
            ].tolist()[0]
            data_dictionary_insert = [
                {
                    "field_name": f"{field_name}___{clean_option}",
                    "field_label": field_option,
                    "field_type": "boolean",
                    "field_unit": np.nan,
                    "field_options": np.nan,
                    "field_skip_logic": data_dictionary.loc[idx, "field_skip_logic"],
                    "parent_field_name": data_dictionary.loc[idx, "field_name"],
                    "section": data_dictionary.loc[idx, "section"],
                    "table_name": table_name,
                    "phase": data_dictionary.loc[idx, "phase"]
                }
                for field_option, clean_option in mapping.items()
            ]
            data_dictionary_inserts[idx] = (
                pd.DataFrame.from_dict(data_dictionary_insert)[data_dictionary.columns]
            )

        # Add all data dictionary inserts in one go
        data_dictionary_list = []
        start_idx = 0
        for idx in sorted(data_dictionary_inserts):
            # Add data_dictionary up to next insert
            data_dictionary_list.append(data_dictionary.iloc[start_idx:idx + 1])
            # Add next insert
            data_dictionary_list.append(data_dictionary_inserts[idx])
            start_idx = idx + 1
        data_dictionary_list.append(data_dictionary.iloc[start_idx:])

        data_dictionary = pd.concat(data_dictionary_list, ignore_index=True)

        setattr(self.data, table_name, df)
        self.data.data_dictionary = data_dictionary
        logger.info("Completed one-hot-encoding fields: %s", ", ".join(valid_field_names))

        if self.validate:
            self.data.validate()
        return self.data

    def inverse_one_hot_encode(
        self,
        table_name: str,
        field_names: List[str],
    ) -> IsaricData:
        return

    def categorical_ynu_to_boolean(
        data: IsaricData,
        table_name: str,
        field_names: List[str],
    ) -> IsaricData:
        return


_METHODS: Dict[str, Callable] = {
    "one-hot-encode": Encoder.one_hot_encode,
    "inverse-one-hot-encode": Encoder.inverse_one_hot_encode,
    "categorical_ynu-to-boolean": Encoder.categorical_ynu_to_boolean,
}


def encode(
    data: IsaricData,
    method: str,
    table_name: str,
    field_names: List[str],
    validate: bool = True,
    inplace: bool = False,
    *args,
    **kwargs,
) -> IsaricData:
    """Wrapper for Encoder class methods."""

    try:
        unbound_func = _METHODS[method]
    except KeyError:
        raise ValueError(
            f"Unknown method {method!r}. Valid methods: {sorted(_METHODS)}"
        )

    encoder = Encoder(data=data, validate=validate, inplace=inplace)
    # Bind the method to the instance
    bound_func = unbound_func.__get__(encoder, type(encoder))

    # The class methods should all have "table_name" and "field_names" as arguments
    # but use inspect to exclude these if they don't exist or no kwargs
    merged_kwargs = {
        **{"table_name": table_name, "field_names": field_names},
        **kwargs,
    }

    spec = inspect.getfullargspec(bound_func)
    if spec.varkw is None:
        accepted_args = set(spec.args) | set(spec.kwonlyargs)
        merged_kwargs = {k: v for k, v in merged_kwargs.items() if k in accepted_args}

    return bound_func(*args, **merged_kwargs)
