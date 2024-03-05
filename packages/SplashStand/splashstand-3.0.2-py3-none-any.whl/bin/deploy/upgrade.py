from contextlib import suppress
from pathlib import Path

from acb.actions.encode import dump
from acb.actions.encode import load
from acb.config import Config
from acb.depends import depends

# from google.cloud.storage import Client

basedir = Path()

whiskeypath = Path("/Users/les/Projects/SplashStand/splashstand/whiskey")

whiskey_scss = whiskeypath / "templates" / "fender" / "scss"
bulma_scss = whiskeypath / "templates" / "bulma"

base_settings = basedir / "base.yml"

base = load.yaml(base_settings)

del_config = [
    "location",
    "mail_server",
    "facebook_app_id",
    "facebook_app_secret",
    "slack_api_key",
    "google_analytics_global_tracker",
    "mail_test_receiver",
]  # add admin_email next upgrade and maybe mail_default_sender

try:
    if not base["gmail_enabled"]:
        del_config.extend(["mail_username", "mail_password"])
except KeyError:
    del_config.extend(["mail_username", "mail_password"])

for c in del_config:
    with suppress(KeyError):
        del base[c]

config = depends.get(Config)

base["mail_default_sender"] = f"info@{config.mail.domain}"

dump.yaml(base, base_settings)


# with suppress(KeyError):
#     base["domain"] = base.pop("url")
#     base["project"] = "splashstand-255421"
#     base["location"] = "us-central1"
# pprint(base)
# dump.yaml(base, base_settings)


# client = Client()


# with suppress(FileNotFoundError):
#     (basepath / "settings").unlink()
#
# for p in [p for p in plugins.iterdir() if p.is_file()]:
#     text = p.read_text()
#     replace_strings = [['.id"))', '.id", ondelete="cascade"))']]
#     for r in replace_strings:
#         if r[0] in text:
#             print(f"Replacing {r[0]} in {p.name}")
#             text = text.replace(r[0], r[1])
#     p.write_text(text)
#
#
# delete_me = [
#     "widget.yml",
#     "widget._scss",
#     "widget.scss",
#     "widget.css",
#     "widget.css.map",
#     "widget.min.css",
#     "custom.min.css",
#     "default.css",
#     "default.css.map",
#     "default.min.css",
#     "form.scss",
#     "form.css",
#     "form.css.map",
#     "form.min.css",
# ]
# for d in delete_me:
#     with suppress(FileNotFoundError):
#         (theme() / "scss" / d).unlink()
#
#
# for f in ["default.yml"]:
#     path = theme() / "scss" / f
#     if not path.exists():
#         if f == "default.yml":
#             copy2(bulma_scss / "fender.yml", path)
#             (theme() / "scss" / "default.scss").rename("default._scss")
#
#
def fix_templates() -> None:
    for p in [p for p in config.templates.app.theme.rglob("*") if p.is_file()]:
        text = p.read_text()
        replace_strings = [
            ["site_url", "config.SITE_URL"],
            ["site_title", "site('title')"],
            ["favicon", "site('favicon')"],
            ["app_icon", "site('app_icon')"],
            ["nav_pages", "config.NAV_PAGES"],
            ["widget_background_image", "config.WIDGET_BACKGROUND_IMAGE"],
            ["comp.get_map", "elem.google_map"],
        ]
        for r in replace_strings:
            if r[0] in text:
                print(f"Replacing {r[0]} in {p.name}")
                text = text.replace(r[0], r[1])
        p.write_text(text)


if __name__ == "__main__":
    fix_templates()
