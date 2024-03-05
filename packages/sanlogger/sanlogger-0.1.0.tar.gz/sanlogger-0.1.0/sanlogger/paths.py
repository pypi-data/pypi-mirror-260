from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
MAIN_DIR = PACKAGE_DIR.parent

# other directories
CONFIG_DIR = MAIN_DIR / 'configuration'
CONFIG_FILE = 'slogger.yaml'
CONFIG_FILEPATH = CONFIG_DIR / CONFIG_FILE

TEMP_DIR = MAIN_DIR / ".temp"
TEMP_DIR.mkdir(exist_ok=True)
