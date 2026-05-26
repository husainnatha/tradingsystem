import os
import importlib

environments = [

    "dev",
    "test",
    "prod"
]

for env in environments:

    print(
        f"\n{'='*40}"
    )

    print(
        f"\nInitializing {env.upper()}"
    )

    print(
        f"\n{'='*40}"
    )

    # -----------------------------------
    # SET ENVIRONMENT
    # -----------------------------------

    os.environ[
        "APP_ENV"
    ] = env

    # -----------------------------------
    # RELOAD ENV MODULES
    # -----------------------------------

    import app.config.environment
    import app.database.db

    importlib.reload(
        app.config.environment
    )

    importlib.reload(
        app.database.db
    )

    # -----------------------------------
    # INITIALIZE DB
    # -----------------------------------

    from app.database.models import (
        Base
    )

    from app.database.db import (
        engine
    )

    Base.metadata.create_all(

        bind=engine
    )

    print(
        "\nDatabase initialized"
    )

    # -----------------------------------
    # IMPORT DATA
    # -----------------------------------

    from scripts.import_transactions import (
        import_transactions
    )

    import_transactions()

    print(
        "\nTransactions imported"
    )

    # -----------------------------------
    # RUN PIPELINE
    # -----------------------------------

    from app.pipeline.run_pipeline import (
        run_pipeline
    )

    run_pipeline()

    print(
        "\nPipeline complete"
    )

print(

    f"\n{'='*40}"

)

print(
    "\nSystem initialization complete\n"
)