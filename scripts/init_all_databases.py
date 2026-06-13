import os
import sys
import subprocess

environments = [

    "dev",
    "test",
    "prod"
]

python_exe = sys.executable

for env in environments:

    print(
        "\n========================================"
    )

    print(
        f"\nInitializing {env.upper()}\n"
    )

    print(
        "========================================\n"
    )

    # -----------------------------------
    # SET ENVIRONMENT
    # -----------------------------------

    #os.environ["APP_ENV"] = env

    env = (

            os.environ("APP_ENV")

            or "test"
        )

    # -----------------------------------
    # INIT DB
    # -----------------------------------

    subprocess.run(

        [

            python_exe,
            "-m",
            "scripts.init_db"

        ],

        env=os.environ.copy()
    )

    # -----------------------------------
    # IMPORT DATA
    # -----------------------------------

    subprocess.run(

        [

            python_exe,
            "-m",
            "scripts.import_transactions"

        ],

        env=os.environ.copy()
    )

    # -----------------------------------
    # RUN PIPELINE
    # -----------------------------------

    subprocess.run(

        [

            python_exe,
            "-m",
            "app.pipeline.run_pipeline"

        ],

        env=os.environ.copy()
    )

print(

    "\n========================================"
)

print(

    "\nSystem initialization complete\n"
)

print(

    "========================================"
)