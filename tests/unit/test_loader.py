from pathlib import Path

import pandas as pd
import pytest
import json
import tempfile

from isaricanalytics.loader.io import Loader, load_data_from_file
from isaricanalytics.data.core import IsaricData


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "data"


def test_loader_init():
    """Test loader correctly initialises"""
    loader = Loader(path=str(FIXTURES))
    assert loader.path == FIXTURES
    assert loader.encoding == "utf-8"
    assert loader.metadata is None
    assert loader.data_dictionary is None

    alt_encoding = 'latin-1'
    loader = Loader(path=str(FIXTURES), encoding=alt_encoding)
    assert loader.encoding == alt_encoding

    with pytest.raises(FileNotFoundError):
        Loader(path=str(FIXTURES / "false_dir"))

    with pytest.raises(TypeError):
        Loader(path=False)

    with pytest.raises(TypeError):
        Loader(path=str(FIXTURES), encoding=False)


def test_loader_metadata():
    """:method:`load_metadata` imports correctly.
    Further tests against metadata schema are in test_data.py"""
    loader = Loader(path=str(FIXTURES))
    print(loader.path)
    loader.load_metadata()
    assert isinstance(loader.metadata, dict)
    expected_files = ("presentation", "outcome", "data_dictionary", "daily", "events")
    assert all(file in loader.metadata["files"] for file in expected_files)
    expected_event_files = ("medication")
    assert expected_event_files in loader.metadata["files"]["events"]


def test_loader_metadata_json():
    """:method:`load_metadata` imports a valid JSON file into a dict."""
    # Valid JSON
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir) / "metadata.json"
        tmp_metadata = {"name": "test"}
        tmpfile.write_text(json.dumps(tmp_metadata), encoding="utf-8")
        loader = Loader(path=str(tmpdir))
        metadata = loader.load_metadata()
        assert metadata == tmp_metadata
        assert loader.metadata == tmp_metadata

    # Invalid JSON
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir) / "metadata.json"
        tmpfile.write_text('{"name": "test",}', encoding="utf-8")
        loader = Loader(path=str(tmpdir))
        with pytest.raises(json.JSONDecodeError):
            loader.load_metadata()


def test_loader_metadata_path():
    """:method:`load_metadata` raises exception if field `path` is invalid"""
    # Invalid JSON
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir) / "metadata.json"
        tmp_metadata = {"name": "test", "path": "wrong_path"}
        tmpfile.write_text(json.dumps(tmp_metadata))
        loader = Loader(path=str(tmpdir))
        with pytest.raises(ValueError):
            loader.load_metadata()


def test_loader_metadata_encoding():
    """Valid encodings for :method:`load_metadata`"""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir) / "metadata.json"
        tmp_metadata = {"name": "test français"}
        tmpfile.write_text(json.dumps(tmp_metadata, ensure_ascii=False), encoding="latin-1")
        loader = Loader(str(tmpdir), encoding='utf-8')
        with pytest.raises(UnicodeDecodeError):
            loader.load_metadata()

        loader = Loader(str(tmpdir), encoding="latin-1")
        loader.load_metadata()
        assert tmp_metadata == loader.metadata

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = Path(tmpdir) / "metadata.json"
        tmp_metadata = {"name": "test français"}
        tmpfile.write_text(json.dumps(tmp_metadata, ensure_ascii=False), encoding="utf-8")

        loader = Loader(str(tmpdir), encoding="utf-8")
        loader.load_metadata()
        assert tmp_metadata == loader.metadata

        loader = Loader(str(tmpdir), encoding="latin-1")
        loader.load_metadata()
        assert tmp_metadata != loader.metadata


def test_loader_data_dictionary():
    """:method:`load_data_dictionary` imports correctly.
    Further tests against data_dictionary schema are in test_data.py"""
    loader = Loader(path=str(FIXTURES))

    with pytest.raises(ValueError):
        loader.load_data_dictionary()  # metadata must be loaded first

    loader.load_metadata()
    assert loader.metadata["files"]["data_dictionary"]["filename"] == "data_dictionary.csv"
    assert loader.metadata["files"]["data_dictionary"]["encoding"] == "utf-8"
    data_dictionary = loader.load_data_dictionary()
    assert isinstance(loader.data_dictionary, pd.DataFrame)
    assert data_dictionary.equals(loader.data_dictionary)

    loader.load_metadata()
    loader.metadata["files"]["data_dictionary"] = {}
    loader.load_data_dictionary()
    assert isinstance(loader.data_dictionary, pd.DataFrame)

    data_dictionary = pd.DataFrame()

    loader.load_metadata()
    loader.metadata["files"]["data_dictionary"]["filename"] = False
    with pytest.raises(TypeError):
        loader.load_data_dictionary()

    loader.load_metadata()
    loader.metadata["files"]["data_dictionary"]["encoding"] = False
    with pytest.raises(TypeError):
        loader.load_data_dictionary()


def test_loader_df():
    """:method:`load_df` imports correctly.
    Further tests against each table schema are in test_data.py"""
    loader = Loader(path=str(FIXTURES))

    with pytest.raises(ValueError):
        loader.load_df("presentation")  # metadata and data_dictionary must be loaded first

    loader.load_metadata()
    with pytest.raises(ValueError):
        loader.load_df("presentation")  # data_dictionary must be loaded first
    loader.load_data_dictionary()

    # required data_dictionary columns
    assert "table_name" in loader.data_dictionary.columns
    assert "field_type" in loader.data_dictionary.columns
    assert "field_name" in loader.data_dictionary.columns

    assert isinstance(loader.load_df("presentation"), pd.DataFrame)

    assert loader.load_df("fakefile") is None  # file doesn't exist, nothing loaded

    # If metadata for e.g. "presentation" is missing a filename, it should still
    # load if a file of the same name exists
    loader.metadata["files"]["presentation"] = {"schema": "schema/presentation.json"}
    assert isinstance(loader.load_df("presentation"), pd.DataFrame)

    loader.metadata["files"]["presentation"] = {"filename": False}
    with pytest.raises(TypeError):
        loader.load_df("presentation")

    loader.metadata["files"]["presentation"]["encoding"] = False
    with pytest.raises(TypeError):
        loader.load_df("presentation")


def test_loader_missing_files():
    """Check if exceptions raised when files are missing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        loader = Loader(path=str(tmpdir))
        with pytest.raises(FileNotFoundError):
            loader.load_metadata()

        loader.metadata = {"name": "test", "files": {}}
        loader.metadata["files"]["data_dictionary"] = {"filename": "data_dictionary"}
        with pytest.raises(FileNotFoundError):
            loader.load_data_dictionary()

        loader.metadata["files"]["presentation"] = {"filename": "presentation"}
        loader.data_dictionary = pd.DataFrame()
        with pytest.raises(FileNotFoundError):
            loader.load_df("presentation")


def test_loader_wrapper():
    """Check if wrapper works and is an IsaricData object."""
    data = load_data_from_file(str(FIXTURES))
    assert isinstance(data, IsaricData)

    # presentation and outcome are required and should be non-empty
    assert hasattr(data, "presentation") and isinstance(data.presentation, pd.DataFrame)
    assert not data.presentation.empty
    assert hasattr(data, "outcome") and isinstance(data.outcome, pd.DataFrame)
    assert not data.outcome.empty
    assert hasattr(data, "daily") and isinstance(data.daily, pd.DataFrame)
    assert hasattr(data, "events") and isinstance(data.events, dict)
    assert "medication" in data.events and isinstance(data.events["medication"], pd.DataFrame)
