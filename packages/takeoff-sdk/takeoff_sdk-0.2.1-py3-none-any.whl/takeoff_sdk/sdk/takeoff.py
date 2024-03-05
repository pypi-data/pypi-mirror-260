"""Takeoff Object SDK"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
import time

import requests
from loguru import logger

from .schema import TakeoffEnvSetting
from .utils import is_docker_logs_error, is_takeoff_loading, start_takeoff, start_takeoff_with_manifest

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                       Takeoff                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class Takeoff:
    def __init__(self, model_name=None, device=None, use_manifest=False, **kwargs):
        self.model_name = model_name
        self.device = device

        self.models = []
        self.consumer_groups = {}
        self.server_url = None
        self.management_url = None
        self.openai_url = None
        self.container = None

        self.use_manifest = use_manifest

        if not self.use_manifest:
            self.takeoff_config = TakeoffEnvSetting(model_name=model_name, device=device, **kwargs)

    def cleanup(self):
        """Remove the Takeoff container if it exists"""
        if self.container:
            self.container.remove(force=True)

    @classmethod
    def from_config(cls, takeoff_config: TakeoffEnvSetting):
        """Create a Takeoff object from a TakeoffEnvSetting object

        Args:
            takeoff_config (TakeoffEnvSetting): Takeoff configuration

        Returns:
            Takeoff: Takeoff object
        """

        takeoff_args = takeoff_config.model_dump()
        return cls(**takeoff_args)

    @classmethod
    def from_manifest(cls, manifest_path: str, device: str = "cuda"):
        """Create a Takeoff object from a manifest file

        Args:
            manifest_path (str): path to the manifest file
            device (str, optional): device choice. Defaults to "cuda".

        Raises:
            FileNotFoundError: if the manifest file is not found

        Returns:
            Takeoff: Takeoff object
        """

        # turns the user input manifest path into an absolute path
        manifest_path = os.path.abspath(manifest_path)

        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found at {manifest_path}")

        cls.manifest_path = manifest_path

        return cls(device=device, use_manifest=True)

    def start(self):
        """Start the Takeoff server and add the model to the primary consumer group"""

        logger.info("Starting Takeoff server...")
        if self.use_manifest:
            logger.info(f"Using manifest file: {self.manifest_path}")
            self.takeoff_port, self.management_port, self.openai_port, self.container = start_takeoff_with_manifest(
                self.manifest_path, self.device
            )
        else:
            self.takeoff_port, self.management_port, self.openai_port, self.container = start_takeoff(
                self.takeoff_config
            )

        self.server_url = f"http://localhost:{self.takeoff_port}"
        self.management_url = f"http://localhost:{self.management_port}"
        self.openai_url = f"http://localhost:{self.openai_port}"

        logger.info(f"Takeoff server running at: {self.server_url}")
        logger.info(f"Takeoff management server running at: {self.management_url}")
        logger.info(f"Takeoff openai compatible server running at: {self.openai_url}")

        for _ in range(100):  # Some models take a while to download
            if not is_takeoff_loading(self.server_url):
                break

            traceback = is_docker_logs_error(self.container)

            if traceback is not None:
                logger.error("Takeoff server failed to start. Error in docker logs. Cleaning up...")
                self.cleanup()
                raise Exception(
                    "Takeoff server failed to start due to error in docker logs. See below for details. \n" + traceback
                )
            logger.info("building...")
            time.sleep(3)
        else:
            raise Exception("Takeoff server build timed out")

        logger.info("server ready!")

        readers = self.readers()
        for group, details in readers.items():
            model_name = details[0]["model_name"]  # Assume one model for each group for now
            self.consumer_groups[model_name] = group
            self.models.append(model_name)

    def add_model(self, model_name: str, backend: str, device: str, consumer_group: str = "primary"):
        """Spawn a new reader for the given model and add it to the given consumer group

        Args:
            model_name (str): model name
            backend (str): backend
            device (str): device
            consumer_group (str, optional): consumer group. Defaults to "primary".
        """
        response = requests.post(
            self.management_url + "/reader",
            json={"model_name": model_name, "device": device, "backend": backend, "consumer_group": consumer_group},
        )
        assert response.ok
        self.models.append(model_name)
        self.consumer_groups[model_name] = consumer_group
        logger.info(f"Added model {model_name} to consumer group {consumer_group}")

    def readers(self):
        response = requests.get(self.management_url + "/reader_groups")
        return response.json()
