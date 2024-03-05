import asyncio
import typing as t
from inspect import stack
from random import choice
from random import randrange
from random import sample
from string import digits

from acb.adapters import import_adapter
from acb.config import Config
from acb.debug import debug
from acb.depends import depends
from aioconsole import ainput
from aioconsole import aprint
from alive_progress import alive_bar
from alive_progress import config_handler
from faker import Faker  # type: ignore
from inflection import humanize
from inflection import pluralize
from inflection import tableize
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel

Logger = import_adapter()
Models = import_adapter()
Sql = import_adapter()


class Demo(BaseModel):
    fake: Faker = Faker()
    config: Config = depends()  # type: ignore
    models: Models = depends()  # type: ignore
    sql: Sql = depends.get(Sql)  # type: ignore
    logger: Logger = depends.get(Logger)  # type: ignore

    def image_dimensions(self) -> tuple[str, str]:
        dimensions = choice(  # nosec B311
            [
                "2500x1406",
                "1920x1080",
                "1600x900",
                "1600x500",
                "1280x720",
                "250x250",
                "150x150",
                "250x100",
                "100x100",
                "1200x630",
                "720x720",
                "800x1200",
                "900x1200",
                "640x480",
                "1080x1080",
                "1080x720",
            ]
        ).split("x")
        return dimensions[0], dimensions[1]

    image_categories: list[str] = [
        "any",
        "animals",
        "architecture",
        "bacon",
        "kittens",
        "nature",
        "people",
        "tech",
    ]

    image_filters: list[str] = ["normal", "grayscale", "sepia"]

    async def get_demo_params(self) -> str:
        options_list = stack()[1][3]
        await aprint(f"\n\nChoose {humanize(options_list).lower()}:\n")
        options = globals()[tableize(options_list)]
        for i, c in enumerate(options):
            await aprint(f"\t{i})  {c}")
        index = await ainput("\nSelect [0]: ")
        index = 0 if index not in digits or not len(index) else int(index)
        return options[index] if index in range(len(options)) else options[0]

    async def image_category(self) -> str:
        img_category = await self.get_demo_params()
        return "arch" if img_category == "architecture" else img_category

    async def image_filter(self, category: str) -> str:
        img_filter = ""
        if category not in ("kittens", "bacon"):
            img_filter = await self.get_demo_params()
        return img_filter if img_filter != "normal" else ""

    @staticmethod
    def image_url(category: str) -> str:
        match category:
            case "kitten":
                return "placekitten.com"
            case "bacon":
                return "baconmockup.com"
            case _:
                ...
        return "placeimg.com"

    async def get_image(self, url: str, category: str, filter: str) -> t.Any:
        w, h = self.image_dimensions()
        placeholder_url = f"https://{url}/{w}/{h}/{category}/{filter}"
        debug(placeholder_url)
        return self.models.ImageObject(  # type: ignore
            name=" ".join(self.fake.words()).title(),
            image=self.fake.image_url(
                height=h, width=w, placeholder_url=placeholder_url
            ),
            description=self.fake.text(max_nb_chars=80),
        )

    async def get_person(self) -> SQLModel:
        return self.models.Person(  # type: ignore
            name=self.fake.name(),
            gmail=f"{self.fake.user_name()}@gmail.com",
            is_superuser=self.fake.pybool(),
            email=self.fake.safe_email(),
        )

    async def get_place(self) -> SQLModel:
        return self.models.Place(  # type: ignore
            name=" ".join(self.fake.words()).title(),
            address=self.fake.address(),
            description=self.fake.text(),
            url=self.fake.url(),
        )

    async def get_event(self) -> SQLModel:
        return self.models.Event(  # type: ignore
            name=" ".join(self.fake.words()).title(),
            # location=self.fake.address(),
            description=self.fake.text(),
            url=self.fake.url(),
            start_date=self.fake.date_this_decade(after_today=True),
            time=self.fake.time_object(),
            door_time=self.fake.time_object(),
        )

    async def get_news(self) -> SQLModel:
        return self.models.NewsArticle(  # type: ignore
            name=" ".join(self.fake.words()).title(),
            address=self.fake.address(),
            description=self.fake.text(),
            article_body=" ".join(self.fake.paragraphs()),
            url=self.fake.url(),
        )

    demo_data: list[tuple[t.Any, int, int]] = [
        (get_image, 21, 42),
        (get_person, 3, 42),
        (get_place, 8, 32),
        (get_event, 50, 108),
        (get_news, 8, 35),
    ]

    config_handler.set_global(length=60, title_length=20)  # type: ignore

    async def timed_progressbar(self, count: int) -> None:
        with alive_bar(count, title="Loading demo data...") as bar:
            for _ in range(count):
                await asyncio.sleep(0.085)
                bar()

    async def init(self) -> None:
        Faker.seed(0)

        await self.sql.init(demo=True)
        try:
            debug("Creating admin superuser...")
            await self.models.create_user(
                gmail=self.config.admin.gmail,
                is_superuser=True,
                email=self.config.admin.email,
                role="admin",
            )
        except IntegrityError:
            debug("Admin superuser exists.")
        total_count = 0
        async with self.sql.async_session() as session:
            for d in self.demo_data:
                args = []
                if d[0] == self.get_image:
                    img_category = await self.image_category()
                    img_filter = await self.image_filter(img_category)
                    img_url = self.image_url(img_category)
                    args.extend([img_url, img_category, img_filter])
                    await aprint()
                count = randrange(d[1], d[2])  # nosec B311
                sample(range(d[1], count), k=1)
                total_count += count
                with alive_bar(
                    count,
                    title=f"Creating {pluralize(d[0].__name__.removeprefix('get_'))}..",
                ) as bar:
                    for _ in range(count):
                        session.add(await d[0](*args))
                        await asyncio.sleep(0.025)
                        bar()
            await aprint("\n")
            task_1 = asyncio.create_task(self.timed_progressbar(total_count))
            task_2 = asyncio.create_task(session.commit())
            await asyncio.wait([task_1, task_2])
            await aprint("\nDemo data loaded.\n")

        # refresh_demo_media()
        # get_pages()


class DemoEntries:
    quotes: list[dict[str, str]] = []
    user_data: list[dict[str, str]] = [
        {
            "about": "<p>Hi I&#39;m the Admin. I can do everything the "
            "Owner can do as well as configure global "
            "site settings, manage user roles, and edit "
            "stylesheets & page templates through the "
            "<a href='/admin' target='_blank'>mobile backend web "
            "UI</a>.</p><p>Please contact <a "
            "href='/contact'>sales</a> to schedule a full "
            "demonstration of available SplashStand features and "
            "templates.</p>"
        },
        {
            "about": "<p>Hi I&#39;m the Owner. I can do everything that the "
            "Contributor can do as well as "
            "manage users, filter internally available media, "
            "and view analytics through the "
            "<a href='/admin' target='_blank'>mobile backend web "
            "UI</a>.</p>"
            "<p>Login: &nbsp;owner"
            "<p>Password: &nbsp;owner</p>"
        },
        {
            "about": "<p>Hi I&#39;m the Contributor. I can create, read, "
            "update, and delete events, quotes, headers, videos "
            "news, projects, and venues through the <a "
            "href='/admin' target='_blank'>mobile backend web "
            "UI</a>.</p>"
            "<p>Login: &nbsp;contributor</p>"
            "<p>Password: &nbsp;contributor</p>"
        },
    ]
    header_images: list[str] = []
    header_videos: list[str] = []
    videos_youtube: list[tuple[str, int, int]] = [
        ("tCXGJQYZ9JA", 1, 222),
        ("EgT_us6AsDg", 0, 0),
        ("NZKXkD6EgBk", 3, 0),
        ("n-D1EB74Ckg", 38, 142),
        ("CevxZvSJLk8", 0, 0),
    ]
    # videos_vimeo = [
    #     ('65891667', 0, 0)
    #     ('26889717', 0, 0)
    #     ('133805386', 0, 0)
    # ]
    site_fields: dict[str, str] = dict(
        about_image_1="",
        app_icon="",
        favicon="",
        nav_logo="",
        header_logo="",
        about="",
        intro="<p>Welcome to the SplashStand demo! This is a working "
        "demo of our mobile-first modular mini-CMS platform and some "
        "of it's features. The database will rebuild it every half "
        "hour on the half hour so feel free to upload images, add/change "
        "content, etc.</p>",
    )


de = DemoEntries

# def get_pages():
#     if not site.is_deployed:
#         from main import app
#         test_app = app.test_client()
#         for page in settings.pages:
#             logger.debug("Fetching '{}' .....".format(page))
#             if page == "index":
#                 test_app.get("/")
#             else:
#                 test_app.get("/{}/".format(page))
#         logger.info("Demo build complete.")
#     else:
#         redis.flushdb()
#         for page in self.config.pages:
#             print("Fetching '{}' .....".format(page))
#             if page == "index":
#                 got = get(f"{self.config.site_url}")
#                 print(got.status_code)
#             else:
#                 got = get(f"{self.config.site_url}/{page}")
#                 print(got.status_code)
#     return True


# def refresh_demo_media():
#     # backup demo media?
#     clear_resized_images()
#     print("Resized images cleared.")
# bucket_data = [Path(b.name) for b in stor.media.list()]
# pprint([b for b in bucket_data])
# test_data = [Path(b.name) for b in stor.media.list(prefix="test")]
# pprint([b for b in test_data])
# for p in bucket_data:
#     if p.name not in [b.name for b in test_data]:
#         name = "/".join(p.parts[1:])
#         print("Deleting: ", name)
#         stor.media.delete(p)
# for p in test_data:
#     if p.name not in [b.name for b in bucket_data]:
#         new_name = "/".join(p.parts[1:])
#         print("Copying: ", p, new_name)
#         stor.media.copy(p, new_name=new_name)
# bucket_data = list(stor.media.list())
# if len(bucket_data) != len(test_data):
#     raise SystemExit("Bucket lengths do not match")
# print("Demo data refreshed.")
# return True


# noinspection PyUnresolvedReferences


if __name__ == "__main__":
    # refresh_demo_media()
    asyncio.run(Demo().init())
