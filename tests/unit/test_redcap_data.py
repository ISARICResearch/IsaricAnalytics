# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pandas as pd
from pandas.testing import assert_frame_equal

# -- Internal libraries --
from isaricanalytics.redcap_data import (
    load_countries_table,
    load_units_conversion_table,
)


class TestLoadUnitsConversionTable:
    def test_load_units_conversion_table(self, conversion_table: pd.DataFrame):
        expected_table = conversion_table
        received_table = load_units_conversion_table()
        assert_frame_equal(received_table, expected_table)


class TestLoadCountriesTable:
    def test_load_countries_table(self, countries: pd.DataFrame):
        expected_table = countries
        received_table = load_countries_table(encoding="latin-1")
        assert_frame_equal(received_table, expected_table)
