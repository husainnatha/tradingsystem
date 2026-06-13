from pathlib import Path

import yaml

import os


class EnvironmentLoader:

    @staticmethod
    def load():

        env = (

            os.getenv("APP_ENV")

            or "test"
        )

        config = {}

        config_dir = Path(
            "config"
        )

        # Environment

        with open(

            config_dir

            / "environments"

            / f"{env}.yaml",

            "r"

        ) as file:

            config["environment"] = (
                yaml.safe_load(file)
            )

        # Tax

        with open(

            config_dir

            / "tax"

            / f"{env}.yml",

            "r"

        ) as file:

            config["uk_tax_config"] = (
                yaml.safe_load(file)
            )

        # Capital

        with open(

            config_dir

            / "capital"

            / f"{env}.yml",

            "r"

        ) as file:

            config["capital"] = (
                yaml.safe_load(file)
            )

        return config
    
    @staticmethod
    def get_environment():

        return (
            os.getenv("APP_ENV")
            or "test"
        )