# -- IMPORTS --

# -- Standard libraries --
from pathlib import Path

# -- 3rd party libraries --
import pandas as pd
import pytest

# -- Internal libraries --


@pytest.fixture(scope="module")
def countries_filepath() -> pd.DataFrame:
    return Path(__file__).parent.joinpath("unit", "assets", "countries.csv")


@pytest.fixture(scope="module")
def countries(countries_filepath) -> pd.DataFrame:
    return pd.read_csv(countries_filepath, encoding="latin-1")


@pytest.fixture(scope="module")
def conversion_table_filepath() -> pd.DataFrame:
    return Path(__file__).parent.joinpath("unit", "assets", "conversion_table.csv")


@pytest.fixture(scope="module")
def conversion_table(conversion_table_filepath) -> pd.DataFrame:
    return pd.read_csv(conversion_table_filepath, encoding="latin-1")
