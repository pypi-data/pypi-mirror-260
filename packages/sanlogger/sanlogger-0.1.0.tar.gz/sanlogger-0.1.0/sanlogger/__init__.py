from .logging import _SLogger as SLogger

from .paths import CONFIG_FILEPATH

from .config_utilities.yaml_utils import create_default_configuration_file


if not CONFIG_FILEPATH.is_file():
    create_default_configuration_file()
