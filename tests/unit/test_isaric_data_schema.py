# -- IMPORTS --

# -- Standard libraries --
import unittest.mock as mock

# -- 3rd party libraries --
# -- Internal libraries --
import isaricanalytics.isaric_transformations as tf
from isaricanalytics.isaric_data_schema import (
    transform_to_isaric_data_schema,
)


class TestTransformToIsaricDataSchema:
    def test_transform_to_isaric_data_schema(self):
        with mock.patch(
            "isaricanalytics.isaric_data_schema.adtl.parse"
        ) as mock_adtl_parse:
            transform_to_isaric_data_schema(
                "fake_custom_parser_file", "fake_custom_data_file"
            )
            mock_adtl_parse.assert_called_once_with(
                "fake_custom_parser_file",
                "fake_custom_data_file",
                include_transform=tf.__file__,
            )
