from acb.config import AppSettings as AppConfigSettings
from acb.adapters import AdapterBase


class AppBaseSettings(AppConfigSettings):
    project: str = "splashstand"
    name: str = "splashstand"
    title: str = "SplashStand"
    style: str = "bulma"
    theme: str = "light"


class AppBase(AdapterBase): ...
