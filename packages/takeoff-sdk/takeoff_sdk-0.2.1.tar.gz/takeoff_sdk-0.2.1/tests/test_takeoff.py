from unittest.mock import MagicMock, patch

import pytest

from takeoff_sdk import Takeoff, TakeoffEnvSetting


def test_takeoff_initialization():
    model_name = "test_model"
    device = "cpu"
    takeoff = Takeoff(model_name=model_name, device=device)

    assert takeoff.model_name == model_name
    assert takeoff.device == device
    assert isinstance(takeoff.takeoff_config, TakeoffEnvSetting)
    assert takeoff.models == []
    assert takeoff.consumer_groups == {}
    assert takeoff.server_url is None
    assert takeoff.management_url is None
    assert takeoff.container is None


def test_takeoff_from_config():
    config = TakeoffEnvSetting(model_name="test_model", device="cpu")
    takeoff = Takeoff.from_config(config)

    assert takeoff.model_name == config.model_name
    assert takeoff.device == config.device


def test_takeoff_from_manifest():
    manifest_path = "tests/test_manifest.yaml"
    takeoff = Takeoff.from_manifest(manifest_path)

    assert takeoff.model_name is None
    assert takeoff.device == "cuda"

    assert takeoff.use_manifest is True


@patch("takeoff_sdk.sdk.takeoff.is_docker_logs_error", return_value=None)
@patch("takeoff_sdk.sdk.takeoff.start_takeoff", return_value=(8000, 8001, 8003, MagicMock()))
@patch("takeoff_sdk.sdk.takeoff.is_takeoff_loading", side_effect=[True, True, False])
def test_takeoff_start(mock_is_loading, mock_start_takeoff, mock_logs_error):
    takeoff = Takeoff(model_name="test_model", device="cpu")

    # Assuming readers() method returns some mock data
    mock_readers = {"group1": [{"model_name": "model1"}]}
    takeoff.readers = MagicMock(return_value=mock_readers)

    takeoff.start()

    assert takeoff.server_url == "http://localhost:8000"
    assert takeoff.management_url == "http://localhost:8001"
    assert "model1" in takeoff.consumer_groups
    assert "model1" in takeoff.models
    mock_start_takeoff.assert_called_once_with(takeoff.takeoff_config)

    assert mock_is_loading.is_called


@patch("takeoff_sdk.sdk.takeoff.is_docker_logs_error", return_value="Error in logs")
@patch("takeoff_sdk.sdk.takeoff.start_takeoff", return_value=(8000, 8001, 8003, MagicMock()))
@patch("takeoff_sdk.sdk.takeoff.is_takeoff_loading", side_effect=[True, True, False])
def test_takeoff_start_error_in_docker_logs(mock_is_loading, mock_start_takeoff, mock_logs_error):
    takeoff = Takeoff(model_name="test_model", device="cpu")

    # Assuming readers() method returns some mock data
    mock_readers = {"group1": [{"model_name": "model1"}]}
    takeoff.readers = MagicMock(return_value=mock_readers)

    with pytest.raises(Exception) as e:
        takeoff.start()
    assert "Takeoff server failed to start due to error in docker logs. See below for details. \nError in logs" in str(
        e.value
    )
