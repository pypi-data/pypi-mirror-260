import typing as t

from acb.adapters import import_adapter
from acb.config import Config
from acb.depends import depends
from pydantic import AnyHttpUrl
from pydantic import AnyUrl
from pydantic import BaseModel

Storage = import_adapter()


class Manifest(BaseModel):
    name: t.Optional[str] = None
    short_name: t.Optional[str] = None
    description: t.Optional[str] = None
    start_url: t.Optional[AnyHttpUrl] = None
    scope: str = "/"
    lang: str = "en-US"
    display: str = "standalone"
    orientation: str = "portrait"
    background_color: str = "#fff"
    theme_color: str = "#fff"
    prefer_related_applications: bool = True
    related_applications: list[dict[str, str]] = [
        dict(platform="play", id="com.app.path")
    ]
    icons: list[dict[str, AnyUrl]] = []


class AppManifest(Manifest):
    @depends.inject
    def __init__(
        self,
        config: Config = depends(),  # type: ignore
        storage: Storage = depends(),  # type: ignore
        **data: t.Any,
    ) -> None:
        super().__init__(**data)
        self.name = config.app.pwa_name
        self.short_name = config.app.pwa_name
        self.description = config.app.title
        self.start_url = config.app.url
        self.background_color = config.app.bgcolor
        self.theme_color = config.app.theme_color
        for s in config.app.icon_sizes.android:
            size = f"{s}x{s}"
            # stock = 0 if self.config.app.icon else 1
            image = config.app.icon or config.admin.icon
            self.icons.append(
                dict(
                    src=storage.media.get_url(
                        image,
                        # resize(size, fit=1, format="png", stock=stock),
                        type="image/png",
                        sizes=size,
                    )
                )
            )


app_manifest = AppManifest()
