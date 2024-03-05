from os import chdir
from pathlib import Path
from pprint import PrettyPrinter
from shutil import copytree
from shutil import ignore_patterns
from string import punctuation
from subprocess import run

from click import command
from click import help_option
from click import option
from acb.actions.encode import dump
from acb.actions.encode import load

pprint = PrettyPrinter(indent=8).pprint

basedir = Path.cwd()

if basedir.name != "projects":
    print("Command must be run from the 'projects' directory.")
    raise SystemExit

whiskey_dir = basedir.parent / "whiskey"
backup_dir = basedir.parent.parent / "BACKUP" / "upgradeproject"


def splashstand_app_name(name: str):
    not_ok = [" ", "_", "."]
    for p in not_ok:
        name = name.replace(p, "-")
    for p in punctuation.replace("-", ""):
        name = name.replace(p, "")
    app = name.strip("-").lower()
    if len(app) < 3:
        raise SystemExit("App name to short.")
    elif len(app) > 63:
        raise SystemExit("App name to long.")
    return app


def cloud_compliant_app_name(name: str):
    not_ok = [" ", "_", "."]
    for p in not_ok:
        name = name.replace(p, "-")
    for p in punctuation.replace("-", ""):
        name = name.replace(p, "")
    app = name.strip("-").lower()
    if len(app) < 3:
        raise SystemExit("App name to short.")
    elif len(app) > 63:
        raise SystemExit("App name to long.")
    return app


# def deploy_revision(app_name):
#     run(f"gcloud builds submit --tag gcr.io/splashstand-255421/{app_name} .".split())
#     settings = dict(
#         # timeout="300",
#         memory="512Mi",
#         # cpu="1000m",
#         max_instances="100",
#         set_cloudsql_instances="splashstand-255421:us-central1:splashstand-mysql",
#     )
#     run(
#         f"gcloud run deploy {app_name} --image gcr.io/splashstand-255421/"
#         f"{app_name} --max-instances {settings['max_instances']} "
#         f"--set-cloudsql-instances {settings['set_cloudsql_instances']} "
#         f"--memory {settings['memory']} --allow-unauthenticated".split()
#     )


def reset_debug(app_dir: Path) -> None:
    debug_file = app_dir / "debug.yml"
    debug_settings = load.yaml(debug_file)
    for k in debug_settings:
        debug_settings[k] = False
    dump.yaml(debug_settings, debug_file)


# def create_zone(project_id, name, dns_name):
#     client = dns_client(project=project_id)
#     zone = client.zone(name, dns_name=dns_name)  # examplezonename  # example.com.
#     zone.create()
#     return zone
#
#
# def add_custom_domain(app_name, domain):  # add custom domain to cloud run
#     domains = run(
#         "gcloud beta run domain-mappings list --format json".split(), stdout=PIPE
#     ).stdout.decode()
#     domains = [d["metadata"]["name"] for d in load.json(domains)]
#     print(domains)
#     if not domain in domains:
#         run(
#             f"gcloud beta run domain-mappings create --service {app_name} --domain "
#             f"{domain}".split()
#         )
#         if len(domain.split(".")) < 3:
#             run(
#                 f"gcloud beta run domain-mappings create --service {app_name}
#                 --domain "
#                 f"www.{domain}".split()
#             )


# set cache db?


def start_project(name: str, deploy: bool = False):
    app_name = cloud_compliant_app_name(name)
    print(f"App name will be:  {app_name}")
    ok = input("Proceed (y/n)?  ")
    if not ok.lower().startswith("y"):
        raise SystemExit
    app_dir = basedir / app_name
    if app_dir.exists() or app_name == "whiskey":
        raise SystemExit("Application directory exists - project creation stopped.")
    title = input("Title: ")
    domain = input("Domain (ie splashstand.org): ")
    if not domain:
        domain = f"{app_name}.splashstand.com"
    mail_domain = input(f"Mail domain [{domain}]: ")
    if not mail_domain:
        mail_domain = domain
    admin_email = input("Admin email [admin@splashstand.com]: ")
    if not admin_email:
        admin_email = "admin@splashstand.com"
    app_pwa_name = input("PWA app name: ")
    admin_pwa_name = input("PWA admin name: ")
    gmail_enabled = False
    is_gmail_enabled = input("Use GMail MX servers [no]: ")
    if is_gmail_enabled.lower().startswith("y"):
        gmail_enabled = True
    ignore_dirs = ["__pycache__", "tmp"]
    ignore_files = [".DS_Store", "mail.yml"]
    ignore = ignore_dirs + ignore_files
    copytree(whiskey_dir, app_dir, ignore=ignore_patterns(*ignore))
    base_settings = dict(
        app_name=app_name,
        domain=domain,
        title=title,
        mail_domain=mail_domain,
        # admin_email=admin_email,
        mail_default_sender=f"info@{mail_domain}",
        app_pwa_name=app_pwa_name,
        admin_pwa_name=admin_pwa_name,
        gmail_enabled=gmail_enabled,
    )
    base_yml = app_dir / "base.yml"
    settings = load.yaml(base_yml)
    for k, v in base_settings.items():
        settings[k] = v
    dump.yaml(settings, base_yml)
    mail_yml = app_dir / "mail.yml"
    mail_yml.touch()
    mail_yml.write_text(f"admin: {admin_email}")
    mail_yml.write_text(f"info: admin@{mail_domain}")
    reset_debug(app_dir)
    if deploy:
        chdir(app_dir)
        run("python {str(basedir / 'deploy' / 'deploy.py'}")  # nosec B607
        # deploy_revision(app_name)
        # add_custom_domain(app_name, domain)
        chdir(basedir)
    return app_name


@command()
@help_option("-h", is_flag=True, help="help")
@option("-c", help="create new project: -c [app_name]")
@option("-d", is_flag=True, help="deploy to gcloud")
def startproject(c: str, d: bool) -> None:
    if c:
        start_project(c, d)


if __name__ == "__main__":
    startproject()
