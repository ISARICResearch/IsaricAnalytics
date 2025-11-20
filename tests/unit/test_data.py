import json
from pathlib import Path
from typing import Union

import pandas as pd
import pytest

from isaricanalytics.data.core import IsaricData

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "data"


def load_fixture_csv(name: str, dtype: Union[str, type] = str) -> pd.DataFrame:
    p = FIXTURES / f"{name}.csv"
    return pd.read_csv(p)


def load_fixture_metadata() -> dict:
    p = FIXTURES / "metadata.json"
    with p.open("r", encoding="utf-8") as json_data:
        return json.load(json_data)


@pytest.mark.unit
def test_post_init():
    metadata = load_fixture_metadata()
    data_dictionary = load_fixture_csv("data_dictionary", dtype=str)
    presentation = load_fixture_csv("presentation")
    outcome = load_fixture_csv("outcome")

    # missing metadata should raise TypeError in __post_init__
    with pytest.raises(TypeError):
        IsaricData(
            metadata=None,  # type: ignore[arg-type]
            data_dictionary=data_dictionary,
            presentation=presentation,
            outcome=outcome,
        )

    # missing metadata should raise TypeError in __post_init__
    with pytest.raises(TypeError):
        IsaricData(
            metadata=metadata,
            data_dictionary=None,  # type: ignore[arg-type]
            presentation=presentation,
            outcome=outcome,
        )

    # missing presentation should raise TypeError in __post_init__
    with pytest.raises(TypeError):
        IsaricData(
            metadata=metadata,
            data_dictionary=data_dictionary,
            presentation=None,  # type: ignore[arg-type]
            outcome=outcome,
        )

    # missing outcome should raise TypeError in __post_init__
    with pytest.raises(TypeError):
        IsaricData(
            metadata=metadata,
            data_dictionary=data_dictionary,
            presentation=presentation,
            outcome=None,  # type: ignore[arg-type]
        )
