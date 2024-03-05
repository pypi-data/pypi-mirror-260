import typing as t

from acb.adapters import import_adapter
from acb.config import Config
from acb.depends import depends
from ..app._manifest import Manifest

Storage = import_adapter()


class AdminManifest(Manifest):
    scope: str = "/admin/"

    @depends.inject
    def __init__(
        self,
        config: Config = depends(),  # type: ignore
        storage: Storage = depends(),  # type: ignore
        **data: t.Any,
    ) -> None:
        super().__init__(**data)
        self.name = config.admin.pwa_name
        self.short_name = config.admin.pwa_name
        self.description = config.admin.title
        self.start_url = config.admin.url
        self.scope = f"/{config.admin.url}/"
        for s in config.app.icon_sizes.android:
            size = f"{s}x{s}"
            # stock = 0 if self.config.app.icon else 1
            image = config.admin.icon
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


admin_manifest = AdminManifest()
