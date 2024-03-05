import pytest
from pydantic import ValidationError

from takeoff_sdk import TakeoffEnvSetting


def test_data_model_with_default_values():
    # Test with default values
    settings = TakeoffEnvSetting(model_name="default_model", device="cpu")
    assert settings.model_name == "default_model"
    assert settings.device == "cpu"

    # assert everything else is None
    for field_name, model_field in settings.__dict__.items():
        if field_name not in ["model_name", "device"]:
            assert model_field is None


def test_settings_to_env_vars_with_custom_values():
    # Test with custom values
    settings = TakeoffEnvSetting(model_name="custom_model", device="cpu", max_batch_size=16)
    env_vars = settings.settings_to_env_vars()
    expected_vars = {"TAKEOFF_MODEL_NAME": "custom_model", "TAKEOFF_DEVICE": "cpu", "TAKEOFF_MAX_BATCH_SIZE": 16}
    assert env_vars == expected_vars


def test_settings_to_env_vars_with_bool_values():
    # Test with bool values, it shoud be converted to lower case string
    settings = TakeoffEnvSetting(model_name="custom_model", device="cpu", disable_continuous_generation=True)
    env_vars = settings.settings_to_env_vars()
    expected_vars = {
        "TAKEOFF_MODEL_NAME": "custom_model",
        "TAKEOFF_DEVICE": "cpu",
        "TAKEOFF_DISABLE_CONTINUOUS_GENERATION": "true",
    }
    assert env_vars == expected_vars


def test_validate_device():
    # Valid devices should not raise an error
    valid_devices = ["cpu", "cuda"]
    for device in valid_devices:
        settings = TakeoffEnvSetting(model_name="test_model", device=device)
        assert settings.device == device

    # Invalid device should raise an error
    with pytest.raises(ValueError) as e:
        TakeoffEnvSetting(model_name="test_model", device="invalid_device")
    assert "device must be either cpu or cuda" in str(e.value)


def test_invalid_attribute():
    # Attempting to create an instance with an undefined attribute should raise an error
    with pytest.raises(ValidationError):
        TakeoffEnvSetting(model_name="test_model", device="cpu", undefined_attribute="value")
