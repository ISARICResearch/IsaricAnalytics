# -- IMPORTS --

# -- Standard libraries --
import unittest.mock as mock

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from bridge.arc.arc_api import ArcApiClientError

from isaricanalytics.isaric_data_schema import (
    IsaricDataSchemaTransformationException,
    transform_to_isaric_data_schema,
)


class TestTransformToIsaricDataSchema:
    def test__no_arc_version__arc_api_exception_on_version_request__isaric_data_schema_transformation_exception_raised(  # noqa: E501
        self,
    ):
        mock_arc_api_client = mock.MagicMock()
        mock_arc_api_client.get_arc_version_list(side_effect=ArcApiClientError)
        with mock.patch(
            "isaricanalytics.isaric_data_schema.adtl.parse",
            return_value="test_ids_tables",
        ) as _:
            with mock.patch(
                "isaricanalytics.isaric_data_schema.ArcApiClient",
                return_value=mock_arc_api_client,
            ) as __:
                with pytest.raises(IsaricDataSchemaTransformationException) as ___:
                    transform_to_isaric_data_schema(
                        "test_parser_file", "test_data_file"
                    )

    def test__no_arc_version__arc_version_list_from_version_request_is_empty__isaric_data_schema_transformation_exception_raised(  # noqa: E501
        self,
    ):
        mock_arc_api_client = mock.MagicMock()
        mock_arc_api_client.get_arc_version_list(return_value=[])
        with mock.patch(
            "isaricanalytics.isaric_data_schema.adtl.parse",
            return_value="test_ids_tables",
        ) as _:
            with mock.patch(
                "isaricanalytics.isaric_data_schema.ArcApiClient",
                return_value=mock_arc_api_client,
            ) as __:
                with pytest.raises(IsaricDataSchemaTransformationException) as ___:
                    transform_to_isaric_data_schema(
                        "test_parser_file", "test_data_file"
                    )

    def test__arc_version__arc_api_exception_on_data_dictionary_request__isaric_data_schema_transformation_exception_raised(  # noqa: E501
        self,
    ):
        with mock.patch(
            "isaricanalytics.isaric_data_schema.adtl.parse",
            return_value="test_ids_tables",
        ) as _:
            with mock.patch(
                "isaricanalytics.isaric_data_schema.get_arc",
                side_effect=ArcApiClientError,
            ) as __:
                with pytest.raises(IsaricDataSchemaTransformationException) as ___:
                    transform_to_isaric_data_schema(
                        "test_parser_file", "test_data_file"
                    )

    def test__arc_version__response_from_arc_data_dictionary_request_is_empty__isaric_data_schema_transformation_exception_raised(  # noqa: E501
        self,
    ):
        with mock.patch(
            "isaricanalytics.isaric_data_schema.adtl.parse",
            return_value="test_ids_tables",
        ) as _:
            with mock.patch(
                "isaricanalytics.isaric_data_schema.get_arc", return_value=tuple()
            ) as __:
                with pytest.raises(IsaricDataSchemaTransformationException) as ___:
                    transform_to_isaric_data_schema(
                        "test_parser_file", "test_data_file"
                    )

    @pytest.mark.skip("WIP")
    def test__arc_version__no_request_exceptions__expected_isaric_data_schema_compliant_tables_returned(  # noqa: E501
        self,
    ): ...
