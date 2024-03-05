import typing as t

from acb.adapters import import_adapter
from acb.config import Config
from acb.config import Settings
from acb.depends import depends
from pydantic import SecretStr

Logger = import_adapter()


class CaptchaBaseSettings(Settings):
    production_key: t.Optional[SecretStr] = None
    dev_key: t.Optional[SecretStr] = None
    threshold: float = 0.5


class CaptchaBase:
    config: Config = depends()
    logger: Logger = depends()  # type: ignore
