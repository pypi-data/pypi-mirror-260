"""
This module contains the data model for the Takeoff SDK. This is used to parse the environment variables
"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

from typing import Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, validator

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                               Configuration Data Model                                               #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["TakeoffEnvSetting"]


class TakeoffEnvSetting(BaseModel):
    """
    This class contains the data model for the Takeoff SDK. This setting is used to set the environment variables
    """

    model_config = ConfigDict(extra="forbid", protected_namespaces=())

    # ------------------------------------- model configuration -------------------------------------- #

    # NOTE: these are expected to be set by the user
    model_name: str = Field(..., env="TAKEOFF_MODEL_NAME")
    device: str = Field(..., env="TAKEOFF_DEVICE")

    backend: Optional[str] = Field(None, env="TAKEOFF_BACKEND")

    max_batch_size: Optional[int] = Field(None, env="TAKEOFF_MAX_BATCH_SIZE")  # 8
    batch_duration_millis: Optional[int] = Field(None, env="TAKEOFF_BATCH_DURATION_MILLIS")  # 100
    access_token: Optional[str] = Field(None, env="TAKEOFF_ACCESS_TOKEN")  # None
    cuda_visible_devices: Optional[str] = Field(None, env="TAKEOFF_CUDA_VISIBLE_DEVICES")  # 0

    refill_threshold: Optional[float] = Field(None, env="TAKEOFF_REILL_THRESHOLD")  # 0.5
    disable_continuous_generation: Optional[bool] = Field(None, env="TAKEOFF_DISABLE_CONTINUOUS_GENERATION")  # False
    consumer_group: Optional[str] = Field(None, env="TAKEOFF_CONSUMER_GROUP")  # primary

    redis_host: Optional[str] = Field(None, env="TAKEOFF_REDIS_HOST")  # localhost
    redis_port: Optional[int] = Field(None, env="TAKEOFF_REDIS_PORT")  # 6379

    heartbeat_wait_interval: Optional[int] = Field(None, env="TAKEOFF_HEARTBEAT_WAIT_INTERVAL")  # 10

    # JF Config
    nvlink_unavailable: Optional[int] = Field(None, env="TAKEOFF_NVLINK_UNAVAILABLE")  # 0

    tensor_parallel: Optional[int] = Field(None, env="TAKEOFF_TENSOR_PARALLEL")  # 1
    disable_cuda_graph: Optional[int] = Field(None, env="TAKEOFF_DISABLE_CUDA_GRAPH")  # 0
    quant_type: Optional[str] = Field(None, env="TAKEOFF_QUANT_TYPE")  # auto, awq
    max_seq_len: Optional[int] = Field(None, env="TAKEOFF_MAX_SEQUENCE_LENGTH")  # 0
    disable_static: Optional[int] = Field(None, env="TAKEOFF_DISABLE_STATIC")  # 0

    export_traces: Optional[bool] = Field(None, env="TAKEOFF_EXPORT_TRACES")  # False
    traces_host: Optional[str] = Field(None, env="TAKEOFF_TRACES_HOST")  # http://localhost:4317
    metrics_target: Optional[str] = Field(None, env="TAKEOFF_METRICS_TARGET")  # redis

    metrics_log_level: Optional[str] = Field(None, env="TAKEOFF_METRICS_LOG_LEVEL")  # INFO

    is_echo: Optional[bool] = Field(None, env="TAKEOFF_ECHO")  # False

    log_level: Optional[str] = Field(None, env="TAKEOFF_LOG_LEVEL")  # INFO
    rust_log_level: Optional[str] = Field(None, env="RUST_LOG")  # INFO

    run_name: Optional[str] = Field(None, env="TAKEOFF_RUN_NAME")  # takeoff_default

    license_key: Optional[str] = Field(None, env="LICENSE_KEY")  # None
    allow_remote_images: Optional[bool] = Field(None, env="TAKEOFF_ALLOW_REMOTE_IMAGES")  # False

    @validator("device")
    def validate_device(cls, v):
        if v not in ["cpu", "cuda", "api"]:
            raise ValueError("device must be one of 'cpu', 'cuda', or 'api'")
        return v

    def settings_to_env_vars(self) -> Dict[str, str]:
        env_var_mapping = {}
        for field_name, model_field in self.__dict__.items():
            field_info = self.model_fields[field_name]
            default_value = field_info.default
            # Only add to env_var_mapping if the current value is different from the default value
            if model_field != default_value:
                if field_info.json_schema_extra is not None and "env" in field_info.json_schema_extra:
                    env_var_name = field_info.json_schema_extra["env"]

                    # Check if the value is of type bool and convert to lowercase string
                    value = model_field
                    if isinstance(value, bool):
                        value = str(value).lower()

                    env_var_mapping[env_var_name] = value

        return env_var_mapping
