from pathlib import Path

import yaml

import os


class EnvironmentLoader:

    @staticmethod
    def load():

        env = os.getenv(
            "APP_ENV",
            "prod"
        )

        path = (

            Path("config")

            / "environments"

            / f"{env}.yaml"
        )

        with open(
            path,
            "r"
        ) as file:

            return yaml.safe_load(file)