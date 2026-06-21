from pathlib import Path
from app.config.environment import BASE_DIR
import app.config.environment as env

def test_check_base_dir ():
    print(BASE_DIR)
    assert True

def test_base_dir():
    expected = Path(env.__file__).resolve().parents[2]
    assert BASE_DIR == expected

    