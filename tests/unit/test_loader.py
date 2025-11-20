from pathlib import Path

import pandas as pd
import pytest

from isaricanalytics.loader.io import Loader, load_data_from_file
from isaricanalytics.data.core import IsaricData


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "data"


@pytest.mark.unit
def test_loader_loads_metadata_and_dictionary():
    project_dir = str(FIXTURES)
    loader = Loader(path=project_dir)
    metadata = loader.load_metadata()
    assert isinstance(metadata, dict)
    assert "files" in metadata

    dd = loader.load_data_dictionary()
    assert isinstance(dd, pd.DataFrame)
    # basic column presence expected in data_dictionary
    for col in ("dataframe_name", "field_name", "field_type"):
        assert col in dd.columns


@pytest.mark.integration
def test_loader_loads_dataframes_and_integration():
    project_dir = str(FIXTURES)

    data = load_data_from_file(project_dir)
    assert isinstance(data, IsaricData)

    # presentation and outcome are required and should be non-empty
    assert hasattr(data, "presentation") and isinstance(data.presentation, pd.DataFrame)
    assert hasattr(data, "outcome") and isinstance(data.outcome, pd.DataFrame)
    assert not data.presentation.empty
    assert not data.outcome.empty

    # optional frames may be present or None, but calling validate() should succeed
    data.validate()
