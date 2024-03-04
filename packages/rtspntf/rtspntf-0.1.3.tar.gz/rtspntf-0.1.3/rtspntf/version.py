import pkg_resources
from .const import PACKAGE_NAME

def get_version() -> str:
    return pkg_resources.get_distribution(PACKAGE_NAME).version
