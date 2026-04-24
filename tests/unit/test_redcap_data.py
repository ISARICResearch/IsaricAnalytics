# -- IMPORTS --

# -- Standard libraries --
import unittest.mock as mock
from pathlib import Path

# -- 3rd party libraries --
import pandas as pd
from pandas.testing import assert_frame_equal

# -- Internal libraries --
from isaricanalytics.redcap_data import (
    load_countries_table,
    load_units_conversion_table,
)


class TestLoadUnitsConversionTable:
    def test_load_units_conversion_table__from_local_assets(self):
        with Path(__file__).parent.parent.parent.joinpath(
            "assets", "conversion_table.csv"
        ) as local_assets_csv_path:
            expected_table = pd.read_csv(
                Path(__file__).parent.joinpath("assets", "conversion_table.csv")
            )

            with mock.patch(
                "isaricanalytics.redcap_data.pd.read_csv",
                mock.MagicMock(return_value=expected_table),
            ) as mock_pd_read_csv:
                received_table = load_units_conversion_table()
                mock_pd_read_csv.assert_called_once_with(local_assets_csv_path)
                assert_frame_equal(received_table, expected_table)

    def test_load_units_conversion_table__from_vertex_github(self):
        with mock.patch(
            "isaricanalytics.redcap_data.Path", side_effect=FileNotFoundError
        ):
            expected_table = pd.read_csv(
                Path(__file__).parent.joinpath("assets", "conversion_table.csv")
            )

            with mock.patch(
                "isaricanalytics.redcap_data.pd.read_csv",
                mock.MagicMock(return_value=expected_table),
            ) as mock_pd_read_csv:
                received_table = load_units_conversion_table()
                mock_pd_read_csv.assert_called_once_with(
                    "https://raw.githubusercontent.com/ISARICResearch/VERTEX/refs/heads/main/assets/conversion_table.csv"
                )
                assert_frame_equal(received_table, expected_table)


class TestLoadCountriesTable:
    def test_load_countries_table__from_local_assets(self):
        with Path(__file__).parent.parent.parent.joinpath(
            "assets", "countries.csv"
        ) as local_assets_csv_path:
            expected_table = pd.read_csv(
                Path(__file__).parent.joinpath("assets", "countries.csv")
            )

            with mock.patch(
                "isaricanalytics.redcap_data.pd.read_csv",
                mock.MagicMock(return_value=expected_table),
            ) as mock_pd_read_csv:
                received_table = load_countries_table(encoding="latin-1")
                mock_pd_read_csv.assert_called_once_with(
                    local_assets_csv_path, encoding="latin-1"
                )
                assert_frame_equal(received_table, expected_table)

    def test_load_countries_table__from_vertex_github(self):
        with mock.patch(
            "isaricanalytics.redcap_data.Path", side_effect=FileNotFoundError
        ):
            expected_table = pd.read_csv(
                Path(__file__).parent.joinpath("assets", "countries.csv")
            )

            with mock.patch(
                "isaricanalytics.redcap_data.pd.read_csv",
                mock.MagicMock(return_value=expected_table),
            ) as mock_pd_read_csv:
                received_table = load_countries_table(encoding="latin-1")
                mock_pd_read_csv.assert_called_once_with(
                    "https://raw.githubusercontent.com/ISARICResearch/VERTEX/refs/heads/main/assets/countries.csv",
                    encoding="latin-1",
                )
                assert_frame_equal(received_table, expected_table)
