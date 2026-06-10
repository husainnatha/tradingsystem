from src.config.environment_loader import (
    EnvironmentLoader
)


class TaxConfigLoader:

    @staticmethod
    def load():

        config = (
            EnvironmentLoader
            .load()
        )

        return config[
            "uk_tax_config"
        ]