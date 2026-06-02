from logging import config

from src.config.capital_config_loader import (
    CapitalConfigLoader
)

from src.services.spreadsheet_capital_loader import (
    SpreadsheetCapitalLoader
)


class CapitalService:

    @staticmethod
    def get_capital_config():

        yaml_config = (
            CapitalConfigLoader
            .load()
        )

        spreadsheet_config = (
            SpreadsheetCapitalLoader
            .load()
        )

        yaml_config.update(
            spreadsheet_config
        )

        print("CONFIG =", yaml_config)
        
        return yaml_config
   
        