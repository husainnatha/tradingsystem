from src.config.environment_loader import (
    EnvironmentLoader
)


class CapitalConfigLoader:

    @staticmethod
    def load():

        config = (
            EnvironmentLoader
            .load()
        )

        return config[
            "capital"
        ]