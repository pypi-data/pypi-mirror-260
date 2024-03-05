import re
import typing as t
from contextlib import suppress
from copy import deepcopy
from datetime import datetime
from datetime import timedelta

import uuid_utils as uuid
from acb.actions.encode import load
from acb.adapters import import_adapter
from acb.config import Config
from acb.debug import debug
from acb.depends import depends
from aiopath import AsyncPath
from fastblocks import current_user

# from asgi_htmx import HtmxRequest
from fastblocks import FastBlocks
from google.oauth2.service_account import Credentials
from inflection import camelize
from inflection import pluralize
from inflection import titleize
from inflection import underscore
from markupsafe import Markup
from pydantic import AnyUrl
from splashstand.adapters.models.main import schema_registry
from sqladmin import Admin as SqlAdmin
from sqladmin import expose
from sqladmin.authentication import login_required  # type: ignore
from sqladmin.helpers import get_object_identifier  # type: ignore
from sqladmin.models import ModelView  # type: ignore
from sqlmodel import select

# from sqlmodel import select  # type: ignore
from sqlmodel import SQLModel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.responses import Response
from starlette_async_jinja import AsyncJinja2Templates
from starlette_async_jinja import JsonResponse
from wtforms.validators import DataRequired  # type: ignore
from ._base import AdminBase
from ._base import AdminBaseSettings

# from wtforms.fields import TextAreaField
# from wtforms.widgets import TextArea
# from wtforms.fields.datetime import DateTimeField


Logger = import_adapter()
Models = import_adapter()
Templates = import_adapter()
Storage = import_adapter()
Sql = import_adapter()


class AdminSettings(AdminBaseSettings):
    title: str = "SplashStand Dashboard"
    style: str = "bulma"
    theme: str = "light"
    pwa_name: str = "SplashBoard"
    roles: t.Optional[list[str]] = ["admin", "owner", "contributor", "viewer"]
    favicon: t.Optional[str] = "SSOutlineTransparent1024-blue.png"
    icon: t.Optional[str] = "IconEditSS1024px-white.png"
    nav_icon: t.Optional[str] = "IconEditSS1024px-blue.png"
    url: t.Optional[str] = "/dashboard"
    logo: t.Optional[str] = "SSComboOutline1024px-blue.png"
    logo_url: t.Optional[AnyUrl] = None
    login_logo: t.Optional[str] = "SSComboOutline1024px-blue.png"
    font: str = "Poppins"
    email: str = "admin@example.com"
    gmail: str = "myemail@gmail.com"
    ios_id: t.Optional[str] = None
    icons: t.Optional[dict[str, str]] = dict(
        content="list",
        store="store",
        site="globe",
        preview="eye",
        analytics="chart-line",
        storage="archive",
        users="users",
        person="users",
        roles="user-shield",
        theme="code",
        cache="piggy-bank",
        change_password="lock",  # nosec B106
        help="question-circle",
        show="eye",
        hide="eye-slash",
        delete="trash",
        top="plus",
        plus_15="angle-double-up",
        plus_5="angle-up",
        minus_5="angle-down",
        minus_15="angle-double-down",
        bottom="minus",
    )


# class AdminKeys:
#     image_keys = dict(
#         # base_path=config.storage_pre,
#         namegen=encode_filename,
#         thumbnail_size=(240, 180, False),
#         allowed_extensions=["png", "jpg", "jpeg"],
#     )
#     video_keys = copy_keys(image_keys, dict(
#           allowed_extensions=["webm", "mp4", "m4v"]))
#     audio_keys = copy_keys(image_keys, dict(allowed_extensions=["m4a", "mp4"]))
#     doc_keys = copy_keys(image_keys, dict(allowed_extensions=["pdf", "doc"]))
#     icon_keys = copy_keys(image_keys, dict(thumbnail_size=(180, 180, False)))
#     # logo_keys = copy_keys(image_keys,
#     #                       dict(thumbnail_size=(240, 135, False)))


# class AdminCKTextAreaWidget(TextArea):
#     def __call__(self, field: str, **kwargs: t.Any) -> t.Any:
#         if kwargs.get("class"):
#             classes = kwargs["class"]
#             kwargs["class"] = classes + " ckeditor"
#         else:
#             kwargs.setdefault("class", "ckeditor")
#         return super(AdminCKTextAreaWidget, self).__call__(field, **kwargs)
#
#
# class AdminCKTextAreaField(TextAreaField):
#     widget: AdminCKTextAreaWidget = AdminCKTextAreaWidget()


class Admin(AdminBase, SqlAdmin):  # type: ignore
    def __init__(self, app: Starlette = FastBlocks(), **kwargs: t.Any) -> None:
        super().__init__(app, **kwargs)

    @depends.inject
    async def init(
        self,
        models: Models = depends(),  # type: ignore
    ) -> None:
        try:
            person = models.Person
            admin_user = await person.query()
            if not len(admin_user):
                self.logger.debug("Creating admin superuser...")
                await models.create_user(
                    gmail=self.config.admin.gmail,
                    is_superuser=True,
                    role="admin",
                )
                admin_user = await person.query()
            for k, v in vars(admin_user[0]).items():
                debug(k, v)
        except Exception as e:
            self.logger.exception(e)

        for model in [m for m in vars(models).values() if issubclass(m, SQLModel)]:
            debug(model)
            # self.add_view(await self.create_view(model))
            self.logger.debug(f"Created {model.__name__} admin view")

    @depends.inject
    @t.override
    def init_templating_engine(
        self, templates: Templates = depends()  # type: ignore
    ) -> AsyncJinja2Templates:
        admin_templates = templates.admin
        admin_templates_env_globals = dict(
            min=min,
            zip=zip,
            admin=self,
            is_list=lambda x: isinstance(x, list),  # type: ignore
            get_object_identifier=get_object_identifier,
        )
        admin_templates.env.globals.update(admin_templates_env_globals)
        return admin_templates

    @t.override
    async def login(  # type: ignore
        self, request: Request
    ) -> t.Coroutine[t.Any, t.Any, t.Any] | RedirectResponse | None:
        if self.authentication_backend:
            context = {}
            ok = await self.authentication_backend.login(request)
            if ok:
                return RedirectResponse(request.url_for("admin:index"), status_code=302)
            context["error"] = "Invalid credentials."
            return await self.templates.TemplateResponse(  # type: ignore
                request, "login.html", context, status_code=200
            )

    @t.override
    async def logout(self, request: Request) -> Response | None:  # type: ignore
        if self.authentication_backend:
            await self.authentication_backend.logout(request)
            return RedirectResponse(request.url_for("admin:index"), status_code=302)

    @login_required
    @expose("/_update_position/<model>", methods=["POST"])  # type: ignore
    async def _update_position(
        self,
        request: Request,
        model_name: str,
        models: Models = depends(),  # type: ignore
    ) -> JsonResponse:
        old_index = int(request.query_params.get("old_index"))  # type: ignore
        new_index = int(request.query_params.get("new_index"))  # type: ignore
        sql_model = getattr(camelize(model_name), models)
        debug(old_index, type(old_index))
        debug(new_index, type(new_index))
        moved_entry = sql_model.query.filter_by(position=old_index)[0]
        if old_index > new_index:
            increments = sql_model.query.filter(
                sql_model.position < old_index, sql_model.position >= new_index
            )
            for i, entry in enumerate(increments):
                entry.position = new_index + i + 1
                entry.save()
        else:
            decrements = sql_model.query.filter(
                sql_model.position <= new_index, sql_model.position > old_index
            )
            for i, entry in enumerate(decrements):
                entry.position = new_index - i - 1
                entry.save()
        moved_entry.position = new_index
        moved_entry.save()
        return JsonResponse({"position": new_index})

    @depends.inject
    @login_required
    @expose("/video_preview/<filename>")  # type: ignore
    def _video_preview(
        self, filename: str, storage: Storage = depends()  # type: ignore
    ) -> Markup:
        return Markup(
            '<video width="1024" height="576" controls'
            ' poster=""><source src="{}" type="video/mp4">'
            "Your browser does not support the video "
            "tag.</video>".format(storage.media.get_url(filename))
        )

    @depends.inject
    @login_required
    @expose("/get_upload_url/<_type>/<_format>/<_extension>")  # type: ignore
    async def get_upload_url(
        self,
        _type: str,
        _format: str,
        _extension: str,
        storage: Storage = depends(),  # type: ignore
    ) -> dict[str, str]:
        upload_credentials = Credentials.from_service_account_info(
            await load.json(self.config.app.google_upload_json),
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )
        upload_key = f"{uuid.uuid7()}.{_extension}"
        content_type = f"{_type}/{_format}"
        presigned_url = storage.get_signed_url(
            AsyncPath(upload_key)
        ).generate_signed_url(
            expiration=timedelta(seconds=120),
            content_type=content_type,
            method="PUT",
            credentials=upload_credentials,
        )
        return dict(url=presigned_url, key=upload_key)

    @login_required
    @expose("/manifest.json")  # type: ignore
    async def manifest(self, request: Request) -> JsonResponse:  # type: ignore
        from ._manifest import admin_manifest

        resp = JsonResponse(
            content=admin_manifest.model_dump_json(), media_type="application/xml"
        )
        resp.headers["Content-Type"] = "application/json"
        resp.headers["Cache-Control"] = "max-age=4200, no-cache, must-revalidate"
        return resp

    @depends.inject
    def get_file_input(
        self, field: t.Any, storage: Storage = depends()  # type: ignore
    ) -> str:
        if field.data and isinstance(field.data, str):
            cloud_fn = storage.media.get_url(field.data)
            # unique_id = field.data.split('.')[0]
            # if field.name == "image":
            #     cloud_fn = stor.media.get_url(resize(field.data, "240x", fit=1))
            html = (
                '<input id="{0}" name="{0}" type="file" '
                'class="file-upload-input" value="{1}" src="{2}"/>'.format(
                    field.name, field.data, cloud_fn
                )
            )
        else:
            html = (
                '<input id="{0}" name="{0}" '
                'class="file-upload-input" type="file">'.format(field.name)
            )
        return Markup(html)

    @depends.inject
    def _list_video_thumbnail(
        self, model: SQLModel, storage: Storage = depends()  # type: ignore
    ) -> Markup | str:
        if model.video:
            input_id = model.video.split(".")[0]
            video_type = model.video.split(".")[1]
            return Markup(
                '<video width="" height="" controls>'
                '<source src="{}" type="video/{}" '
                'preload="metadata" id="video-{}">'
                "Your browser does not support the video tag."
                "</video>".format(
                    storage.media.get_url(model.video), video_type, input_id
                )
            )
        elif "youtube_id" in vars(model):
            if model.youtube_id and not model.video:
                return Markup(
                    '<div class="youtube-iframe" '
                    'style="position:relative;padding-top:56.25%;">'
                    '<iframe width="" height="" '
                    'src="https://www.youtube.com/embed/{0}" '
                    'frameborder="0" allowfullscreen '
                    'style="position:absolute;top:0;left:0;width:100%;height:100%;" '
                    'id="youtube-{0}">'
                    "</iframe>"
                    "</div>"
                ).format(model.youtube_id)
        return ""

    def _list_image_thumbnail(self, model: SQLModel) -> str | Markup:
        image = None
        try:
            image = model.image
        except AttributeError:
            try:
                image = model.photo
            except AttributeError:
                with suppress(AttributeError):
                    image = model.picture
        if not image:
            if "video" in vars(model):
                return self._list_video_thumbnail(model)
            return ""
        input_id = image.split(".")[0]
        # thumb = resize(image, "x240", fit=1)
        return Markup(
            '<a class="image-popup-link" href="{}"><img '
            'id="image-{}" class="list-image" src="{}" />'
            "</a>".format(model.image.url, input_id, model.image.thumbnail_url)
        )

    @depends.inject
    async def create_view(
        self,
        app_model: type[SQLModel],
        config: Config = depends(),  # type: ignore
    ) -> t.Any:  # type: ignore
        last_fields = [
            "visible",
            "maintainer",
            "editor",
            "date_created",
            "date_modified",
        ]

        first_fields = [
            f
            for f in list(schema_registry.get()["thing"].fields.keys())
            if f != "visible"
        ]

        class cls(ModelView, model=app_model):  # type: ignore
            _fields: dict[str, t.Any] = app_model.__model_fields__

            def is_accessible(self, request: Request) -> bool:
                return current_user.get().is_superuser

            def is_visible(self, request: Request) -> bool:
                return True

            @depends.inject
            async def get_entries(
                self, model: SQLModel, sql: Sql = depends()  # type: ignore
            ) -> list[t.Any]:
                async with sql.async_session() as session:
                    entries_query = select(model)  # type: ignore
                    result = await session.execute(entries_query)
                    return result.all()

            async def after_model_change(
                self,
                data: dict[str, t.Any],
                model: t.Any,
                is_created: bool,
                request: Request,
            ) -> None:
                if is_created:
                    entries = await self.get_entries(model)
                    with suppress(AttributeError):
                        for entry in entries:
                            if entry.position == 99999:
                                entry.position = 1
                            else:
                                entry.position = entry.position + 1
                            entry.save()

            async def after_model_delete(self, model: t.Any, request: Request) -> None:
                with suppress(AttributeError):
                    rm_position = model.position
                    entries = await self.get_entries(model)
                    for entry in entries:
                        if entry.position > rm_position:
                            entry.position = entry.position - 1
                            # entry.save()

            async def on_model_change(
                self,
                data: dict[str, t.Any],
                model: t.Any,
                is_created: bool,
                request: Request,
            ) -> None:
                if "youtube_id" in vars(model) and model.youtube_id:
                    for prefix in (
                        "https://youtu.be/",
                        "http://youtu.be/",
                        "https://www.youtube.com/watch?v=",
                        "http://www.youtube.com/watch?v=",
                    ):
                        model.youtube_id = model.youtube_id.lstrip(prefix)
                    pattern = r"[&,?]t=(\d+)"
                    start = re.search(pattern, model.youtube_id)
                    if start and ((not model.start) or model.start == "00:00:00"):
                        model.start = timedelta(seconds=int(start.group(1)))
                    pattern = r"[&,?]t=(\d+).*"
                    model.youtube_id = re.sub(pattern, "", model.youtube_id)
                if "spotify_id" in vars(model) and model.spotify_id:
                    ...
                if "archive_id" in vars(model) and model.archive_id:
                    ...
                if "soundcloud_id" in vars(model) and model.soundcloud_id:
                    ...
                if "bandcamp_id" in vars(model) and model.bandcamp_id:
                    ...

            @staticmethod
            def _datetime_format(value: datetime) -> str:
                # return value.strftime('%m-%d-%Y %I:%M %p')
                # return value.strftime('%a %b %w, %Y - %I:%M %p')
                return value.strftime("%a %b %d, %Y - %I:%M %p")
                # return value.strftime('%a %b %d, %Y')

            # column_type_formatters: dict[str, t.Any] = dict(
            #     ModelView.column_type_formatters, date=_datetime_format
            # )

            column_formatters = {  # type: ignore
                app_model.image: self._list_image_thumbnail,
                app_model.picture: self._list_image_thumbnail,
                app_model.photo: self._list_image_thumbnail,
                app_model.video: self._list_video_thumbnail,
            }

            page_size = 25
            page_size_options = [25, 50, 100, 200]
            can_delete = True
            details_template = "details.html"
            list_template = "list.html"
            form_include_pk = False
            form_args = {}
            form_columns = list(_fields.keys())
            form_columns.remove("id")
            form_columns = [
                f for f in form_columns if f not in last_fields + first_fields
            ]
            form_columns = first_fields + form_columns
            column_details_list = deepcopy(form_columns)
            form_columns.append("visible")
            # form_widget_args = dict(uid=dict(readonly=True))
            # if not current_user.get().has_role(
            #     "admin"
            # ) or not current_user.get().has_role("owner"):
            #     form_widget_args.gmail = dict(readonly=True)
            for name, field in _fields.items():  # noqa: FURB135
                if field.alias != field.name:
                    key_name = name.removesuffix("_pk")
                form_kwargs = dict(label=titleize(field.alias.removesuffix("_pk")))
                if field.required:
                    form_kwargs["validators"] = [DataRequired()]  # type: ignore
                form_args[name] = form_kwargs
            column_list = ["name"]
            if "position" in list(_fields.keys()):
                column_list.remove("position")
                column_default_sort = "position"
                column_sortable_list = ["position"]
                column_list.append("position")
            elif "published" in _fields:
                column_default_sort = ("published", True)
            elif "date" in _fields:
                column_default_sort = "date"
            else:
                column_default_sort = "name"
                column_sortable_list = ["name"]
            column_details_list.extend(last_fields)

        cls.__name__ = f"{app_model.__name__}Admin"
        cls.name = titleize(app_model._alias or cls.name)
        cls.name_plural = pluralize(cls.name)
        cls.icon = f"fa-solid fa-{config.admin.icons[underscore(cls.name)]}"
        debug(cls.__name__)
        debug(vars(cls))
        debug(cls.column_list)
        debug(cls.form_columns)
        debug(cls.column_details_list)
        return cls


depends.set(Admin)

#
#
# class CustomView(BaseView):
#     name = "Custom Page"
#     icon = "fa-chart-line"
#
#     @expose("/custom", methods=["GET"])
#     def custom_page(self, request):
#         return await self.templates.render_template(
#             "custom.html",
#             context={"request": request},
#         )

# def admin_template_args():
#     template_args = dict(
#         admin_module_icons=admin.module_icons,
#         admin_css=render_inline_css(admin_yml),
#     )
#     for t in (admin() / "js").iterdir():
#         template_args[f"admin_{t.stem.lower()}_js"] = str(t.resolve())
#     return template_args

# def render_admin(self, template, **kwargs):
#     # print(request.method)
#     # if request.method == "POST":
#     #     g.save_db = 1
#     template_args = dict(
#         admin_view=self,
#         admin_base_template=self.admin.base_template,
#         get_url=self.get_url,
#     )
#     kwargs.update(template_args)
#     kwargs.update(admin_template_args())
#     kwargs.update(self._template_args)
#     resp = ""
#     try:
#         template = render_template(template, **kwargs)
#     except UndefinedError:
#         cache_templates(admin())
#         template = render_template(template, **kwargs)
#     # if (deployed or debug.production or debug.css)
#           and request.path != self.get_url(
#     #         'cache.execute_view'):
#     if site.is_deployed or debug.production or debug.css:
#         template = remove_unused_css(template)
#     resp = make_response(template)
#     resp.headers["Cache-Control"] = "no-store, must-revalidate, max-age=0"
#     return resp

# elif "column_default_sort" in view_args.keys():
#     setattr(self, "column_default_sort", view_args["column_default_sort"])
# if "column_list" in view_args.keys():
#     column_list = view_args["column_list"]
#     if debug.position:
#         column_list.append("position")
#     if "visible" in fields:
#         column_list.append("visible")
#     setattr(self, "column_list", column_list)
# for field in fields:
#     if field.endswith("_url"):
#         self.form_extra_fields[field] = URLField(
#             field.replace("_", " ").title(), validators=[Optional(), URL()]
#         )
#     elif field.endswith("_phone"):
#         self.form_extra_fields[field] = TelField(
#             field.replace("_", " ").title(), validators=[Optional()]
#         )
# if "form_excluded_columns" in view_args.keys():
#     for field in view_args["form_excluded_columns"]:
#         fields.remove(field)
# for field in last_fields:
#     fields.remove(field)
# fields.extend(["visible"])
# fields.insert(0, "name")
# self.form_columns = fields

# super().__init__()

# def is_action_allowed(self, name):
#     if "position" in fields:
#         if name in (self.allowed_actions + self.position_actions):
#             return super(AdminModelView, self).is_action_allowed(name)
#     else:
#         if name in self.allowed_actions:
#             return super(AdminModelView, self).is_action_allowed(name)

# form_ajax_refs = {
#     "address": {
#         "fields": ("zip_code", "street"),
#         "order_by": ("id",),
#     }
# }

#     if ac.ckeditor_fields:
#         for f in ac.ckeditor_fields:
#             form_overrides[f] = AdminCKTextAreaField
#     if ac.select_fields:
#         for k, v in ac.select_fields.items():
#             # print(k, v)
#             for x, y in v.items():
#                 form_overrides[x] = Select2Field
#                 form_args[x] = dict(
#                     choices=[
#                         (c, c.replace("_", " ").title().replace(
#                         "Youtube", "YouTube"))
#                         for c in y
#                     ]
#                 )
#                 form_widget_args[x] = {"class": "select input"}
#     form_extra_fields = {
#         "image": PluginImageUploadField("Image", **ak.image_keys),
#         "picture": PluginImageUploadField("Picture", **ak.image_keys),
#         "photo": PluginImageUploadField("Photo", **ak.image_keys),
#         "video": AdminFileUploadField("Video", **ak.video_keys),
#         "audio": AdminFileUploadField("Audio", **ak.audio_keys),
#         "brochure": AdminFileUploadField("Brochure", **ak.doc_keys),
#         "email": EmailField("Email", validators=[Optional(), Email()]),
#         "google_email_field": EmailField(
#             "Google Email", validators=[Email(), Optional()]
#         ),
#         "facebook_email_field": EmailField(
#             "Facebook Email", validators=[Email(), Optional()]
#         ),
#         "youtube_id": StringField("YouTube ID"),
#     }

#     column_display_all_relations = True
#     for field in ac.datetime_fields:
#         form_extra_fields[field] = DateTimeField(
#             field.title().replace("_", " "),
#             validators=[DataRequired()],
#             format="%m-%d-%Y %I:%M %p",
#         )
#         form_widget_args[field] = {"data-date-format": ac.datetime_format}
#     allowed_actions = ["show", "hide", "delete"]
#     position_actions = ["top", "plus_15", "plus_5", "minus_5",
#           "minus_15", "bottom"]
#
#     def _available_media(self, model):
#         _avail = []
#         with suppress(AttributeError):
#             _avail = stor.media.list()
#             try:
#                 image_url = get_storage_media_url(model.image)
#             except AttributeError:
#                 try:
#                     image_url = get_storage_media_url(model.photo)
#                 except AttributeError:
#                     with suppress(AttributeError):
#                         image_url = get_storage_media_url(model.picture)
#             for media in _avail:
#                 if media == image_url:
#                     _avail.remove(media)
#         return _avail
#
#     def get_details_columns(self):
#         try:
#             only_columns = self.column_details_list
#               or self.scaffold_list_columns()
#         except NotImplementedError:
#             raise Exception("Please define column_details_list.")
#
#         columns = self.get_column_names(
#             only_columns=only_columns,
#             excluded_columns=self.column_details_exclude_list
#         )
#         new_list = []
#         end_fields = []
#         for c in columns:
#             if c[0] == "name":
#                 new_list.insert(0, c)
#             elif c[0] in [
#                 "created_by",
#                 "created_at",
#                 "last_edited_by",
#                 "last_edited_at",
#                 "visible",
#             ]:
#                 end_fields.append(c)
#             else:
#                 new_list.append(c)
#         new_list.extend(end_fields)
#         return new_list
#
#     def _get_list_value(
#         self, context, model, name, column_formatters, column_type_formatters
#     ):
#         column_fmt = column_formatters.get(name)
#         if column_fmt is not None:
#             value = column_fmt(self, context, model, name)
#         else:
#             value = self._get_field_value(model, name)
#         choices_map = self._column_choices_map.get(name, {})
#         if choices_map:
#             return choices_map.get(value) or value
#         type_fmt = None
#         for typeobj, formatter in column_type_formatters.items():
#             if isinstance(value, typeobj):
#                 type_fmt = formatter
#                 break
#         if type_fmt is not None:
#             value = type_fmt(self, value)
#         with suppress(AttributeError):
#             value = value.all()
#             value = ", ".join([str(v) for v in value])
#         return value
#
#     # Model handlers
#     def create_model(self, form):
#         try:
#             model = self.model()
#             form.populate_obj(model)
#             model.save()
#             self._on_model_change(form, model, True)
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(
#                     gettext("Failed to create record. %(error)s", error=str(ex)),
#                     "error",
#                 )
#                 ca.self.logger.exception("Failed to create record.")
#             self.session.rollback()
#             return False
#         else:
#             self.after_model_change(form, model, True)
#         return True
#
#     def update_model(self, form, model):
#         try:
#             form.populate_obj(model)
#             model.save()
#             self._on_model_change(form, model, False)
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(
#                     gettext("Failed to update record. %(error)s", error=str(ex)),
#                     "error",
#                 )
#                 ca.self.logger.exception("Failed to update record.")
#             self.session.rollback()
#             return False
#         else:
#             self.after_model_change(form, model, False)
#         return True
#
#     def delete_model(self, model):
#         try:
#             self.on_model_delete(model)
#             model.delete()
#             return True
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(
#                     gettext("Failed to delete record. %(error)s", error=str(ex)),
#                     "error",
#                 )
#                 ca.self.logger.exception("Failed to delete record.")
#             self.session.rollback()
#             return False
#
#     def handle_action(self, return_view=None):
#         url = self.get_url(".index_view").rstrip("?") or get_redirect_target()
#         form = self.action_form()
#         if self.validate_form(form):
#             # using getlist instead of FieldList for backward compatibility
#             ids = request.form.getlist("rowid")
#             action = form.action.data
#             handler = self._actions_data.get(action)
#             if debug.action:
#                 print(action, ids)
#             if handler and self.is_action_allowed(action):
#                 response = handler[0](ids)
#                 if response is not None:
#                     # return response
#                     sleep(1)
#                     return jsonify(action=action, ids=ids, url=url)
#             if not action in ["show", "hide"]:
#                 sleep(1)
#             return jsonify(action=action, ids=ids, url=url)
#         else:
#             flash_errors(form, message="Failed to perform action. %(error)s")
#             return jsonify(url=url)
#
#
#     @action("show", lazy_gettext("Show"))
#     def action_show(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for m in query.all():
#                 m.visible = True
#                 count += 1
#                 m.save()
#             # flash(ngettext('1 record now visible.',
#             #                '{} records now visible.'.format(str(count)),
#             #                count),
#             #       'info')
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to show records. {}".format(err), "error")
#
#     @action("hide", lazy_gettext("Hide"))
#     def action_hide(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for m in query.all():
#                 m.visible = False
#                 count += 1
#                 m.save()
#             # flash(ngettext('1 record now hidden.',
#             #                '{} records now hidden.'.format(str(count)),
#             #                count),
#             #       'info')
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to hide records. {}".format(err), "error")
#
#     @action("top", lazy_gettext("Top"))
#     def action_top(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in reversed(query.order_by(self.model.position).all()):
#                 old_position = q.position
#                 new_position = 1
#                 for entry in self.model.query.all():
#                     if (entry.position >= new_position) and (
#                         entry.position < old_position
#                     ):
#                         entry.position = entry.position + 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved to the top.",
#                     "{} records moved to the top.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action("bottom", lazy_gettext("Bottom"))
#     def action_bottom(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in query.order_by(self.model.position).all():
#                 new_position = len(self.model.query.all())
#                 old_position = q.position
#                 for entry in self.model.query.all():
#                     if (entry.position > old_position) and (
#                         entry.position <= new_position
#                     ):
#                         entry.position = entry.position - 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved to the bottom.",
#                     "{} records moved to the bottom.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action("plus_5", lazy_gettext("+5"))
#     def action_plus_5(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in reversed(query.order_by(self.model.position).all()):
#                 old_position = q.position
#                 new_position = old_position - 5
#                 if new_position < 1:
#                     new_position = 1
#                 for entry in self.model.query.all():
#                     if (entry.position >= new_position) and (
#                         entry.position < old_position
#                     ):
#                         entry.position = entry.position + 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved up 5.",
#                     "{} records moved up 5.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action("plus_15", lazy_gettext("+15"))
#     def action_plus_15(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in reversed(query.order_by(self.model.position).all()):
#                 old_position = q.position
#                 new_position = old_position - 15
#                 if new_position < 1:
#                     new_position = 1
#                 for entry in self.model.query.all():
#                     if (entry.position >= new_position) and (
#                         entry.position < old_position
#                     ):
#                         entry.position = entry.position + 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved up 15.",
#                     "{} records moved up 15.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action("minus_5", lazy_gettext("-5"))
#     def action_minus_5(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in query.order_by(self.model.position).all():
#                 last_position = len(self.model.query.all())
#                 old_position = q.position
#                 new_position = old_position + 5
#                 if new_position > last_position:
#                     new_position = last_position
#                 for entry in self.model.query.all():
#                     if (entry.position <= new_position) and (
#                         entry.position > old_position
#                     ):
#                         entry.position = entry.position - 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved down 5.",
#                     "{} records moved down 5.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action("minus_15", lazy_gettext("-15"))
#     def action_minus_15(self, ids):
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             count = 0
#             for q in query.order_by(self.model.position).all():
#                 last_position = len(self.model.query.all())
#                 old_position = q.position
#                 new_position = old_position + 15
#                 if new_position > last_position:
#                     new_position = last_position
#                 for entry in self.model.query.all():
#                     if (entry.position <= new_position) and (
#                         entry.position > old_position
#                     ):
#                         entry.position = entry.position - 1
#                     # db_session.add(entry)
#                     entry.save()
#                 q.position = new_position
#                 q.save()
#                 count += 1
#                 if debug.position:
#                     print("old", old_position, "new", new_position)
#             flash(
#                 ngettext(
#                     "1 record moved down 15.",
#                     "{} records moved down 15.".format(str(count)),
#                     count,
#                 ),
#                 "info",
#             )
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash("Failed to move records. {}".format(err), "error")
#
#     @action(
#         "delete",
#         lazy_gettext("Delete"),
#         lazy_gettext("Are you sure you want to delete the selected " "records?"),
#     )
#     def action_delete(self, ids):
#         count = 0
#         skip = 0
#         try:
#             query = tools.get_query_for_ids(self.get_query(), self.model, ids)
#             if self.fast_mass_delete:
#                 count = query.delete(synchronize_session=False)
#             else:
#                 for q in query.all():
#                     if current_user.id > 2 and q.created_by != current_user.name:
#                         skip += 1
#                         continue
#                     else:
#                         self.delete_model(q)
#                         count += 1
#             flash(
#                 ngettext(
#                     "1 record was successfully deleted.",
#                     "{} records were successfully deleted.".format(str(count)),
#                     count,
#                 ),
#                 "success",
#             )
#             if skip:
#                 flash(
#                     ngettext(
#                         "1 record was not owned by you and was not "
#                         "deleted. (Try 'Hide')",
#                         "{} records were "
#                         "not owned by you and "
#                         "were not deleted. "
#                         "(Try 'Hide')".format(str(skip)),
#                         skip,
#                     ),
#                     "info",
#                 )
#
#         except Exception as err:
#             if not self.handle_view_exception(err):
#                 raise
#             flash(gettext("Failed to delete records.\n{}".format(str(err))),
#               "error")
#
#

# class cls(ModelView):
#     def __init__(self, model, session, name=None, menu_icon_value=None):
#         self.menu_icon_value = menu_icon_value
#         if "position" in fields:
#             setattr(self, "column_default_sort", "position")
#             setattr(self, "column_sortable_list", ["position"])
#         elif "published" in fields:
#             setattr(self, "column_default_sort", ("published", True))
#         elif "date" in fields:
#             setattr(self, "column_default_sort", "date")
#         elif "column_default_sort" in view_args.keys():
#             setattr(self, "column_default_sort", view_args["column_default_sort"])
#         if "column_list" in view_args.keys():
#             column_list = view_args["column_list"]
#             if debug.position:
#                 column_list.append("position")
#             if "visible" in fields:
#                 column_list.append("visible")
#             setattr(self, "column_list", column_list)
#         # for field in fields:
#         #     if field.endswith("_url"):
#         #         self.form_extra_fields[field] = URLField(
#         #             field.replace("_", " ").title(), validators=[Optional(),
#                           URL()]
#         #         )
#         #     elif field.endswith("_phone"):
#         #         self.form_extra_fields[field] = TelField(
#         #             field.replace("_", " ").title(), validators=[Optional()]
#         #         )
#         if "form_excluded_columns" in view_args.keys():
#             for field in view_args["form_excluded_columns"]:
#                 fields.remove(field)
#         for field in last_fields:
#             fields.remove(field)
#         fields.extend(["visible"])
#         fields.insert(0, "name")
#         self.form_columns = fields
#
#         super().__init__(model, session, name=name,
#               menu_icon_value=menu_icon_value)
#
#         def is_action_allowed(self, name):
#             if "position" in fields:
#                 if name in (self.allowed_actions + self.position_actions):
#                     return super(AdminModelView, self).is_action_allowed(name)
#             else:
#                 if name in self.allowed_actions:
#                     return super(AdminModelView, self).is_action_allowed(name)
#
#         cls.__name__ = f"{model}AdminView"
#
#         return cls

# def _setup_templates(self) -> None:
#     templates.env.loader = ChoiceLoader(
#         [
#             FileSystemLoader(self.templates_dir),
#             PackageLoader("starlette_admin", "templates"),
#         ]
#     )
#     # globals
#     templates.env.globals["views"] = self._views
#     templates.env.globals["title"] = self.title
#     templates.env.globals["is_auth_enabled"] = self.auth_provider is not None
#     templates.env.globals["__name__"] = self.route_name
#     templates.env.globals["logo_url"] = self.logo_url
#     templates.env.globals["login_logo_url"] = self.login_logo_url
#     templates.env.globals["custom_render_js"] = lambda r: self.custom_render_js(r)
#     templates.env.globals["get_locale"] = get_locale
#     templates.env.globals["get_locale_display_name"] = get_locale_display_name
#     templates.env.globals["i18n_config"] = self.i18n_config or I18nConfig()
#     # filters
#     templates.env.filters["is_custom_view"] = lambda r: isinstance(r, CustomView)
#     templates.env.filters["is_link"] = lambda res: isinstance(res, Link)
#     templates.env.filters["is_model"] = lambda res: isinstance(res, BaseModelView)
#     templates.env.filters["is_dropdown"] = lambda res: isinstance(res, DropDown)
#     templates.env.filters["get_admin_user"] = (
#         self.auth_provider.get_admin_user if self.auth_provider else None
#     )
#     templates.env.filters["tojson"] = lambda data: json.dumps(data, default=str)
#     templates.env.filters["file_icon"] = get_file_icon
#     templates.env.filters[
#         "to_model"
#     ] = lambda identity: self._find_model_from_identity(identity)
#     templates.env.filters["is_iter"] = lambda v: isinstance(v, (list, tuple))
#     templates.env.filters["is_str"] = lambda v: isinstance(v, str)
#     templates.env.filters["is_dict"] = lambda v: isinstance(v, dict)
#     templates.env.filters["ra"] = lambda a: RequestAction(a)
#     # install i18n
#     templates.env.install_gettext_callables(gettext, ngettext, True)# type: ignore
#     self.templates = templates
