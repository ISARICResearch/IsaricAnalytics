# -- IMPORTS --

# -- Standard libraries --
from pathlib import Path

# -- 3rd party libraries --
import pandas as pd
import pytest

# -- Internal libraries --


@pytest.fixture(scope="module")
def countries() -> pd.DataFrame:
    fp = Path(__file__).parent.joinpath("unit", "assets", "countries.csv")
    assert fp.exists()
    return pd.read_csv(fp, encoding="latin-1")


@pytest.fixture(scope="module")
def conversion_table() -> pd.DataFrame:
    fp = Path(__file__).parent.joinpath("unit", "assets", "conversion_table.csv")
    assert fp.exists()
    return pd.read_csv(fp, encoding="latin-1")


@pytest.fixture(scope="module")
def isaric_data_schema_example_dataset_filepath() -> Path:
    return (
        Path(__file__)
        .parent.joinpath("unit", "assets", "isaric_data_schema_example_dataset.csv")
        .resolve()
    )


@pytest.fixture(scope="module")
def isaric_data_schema_example_parser_filepath() -> Path:
    return (
        Path(__file__)
        .parent.joinpath("unit", "assets", "isaric_data_schema_example_parser.toml")
        .resolve()
    )


@pytest.fixture(scope="module")
def isaric_data_schema_example_core_table_filepath() -> Path:
    return (
        Path(__file__)
        .parent.joinpath("unit", "assets", "isaric_data_schema_example_core_table.csv")
        .resolve()
    )


@pytest.fixture(scope="module")
def isaric_data_schema_example_long_table_filepath() -> Path:
    return (
        Path(__file__)
        .parent.joinpath("unit", "assets", "isaric_data_schema_example_long_table.csv")
        .resolve()
    )


@pytest.fixture(scope="module")
def arc_data_dictionary_v1_5_0() -> pd.DataFrame:
    fp = Path(__file__).parent.joinpath("unit", "assets", "arc_v1.5.0.csv").resolve()
    assert fp.exists()
    return pd.read_csv(fp)
