import typing as t
from base64 import b64encode
from contextlib import suppress
from datetime import timedelta
from time import time

from acb.adapters import import_adapter
from acb.config import Config
from acb.debug import debug
from acb.depends import depends
from fastblocks import current_user
from firebase_admin import auth
from firebase_admin import initialize_app
from google.auth.transport import requests as google_requests
from pydantic import EmailStr
from pydantic import SecretStr
from sqlmodel import select  # type: ignore
from sqlmodel import SQLModel
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from ._base import AuthBase
from ._base import AuthBaseSettings
from ._base import AuthBaseUser

firebase_request_adapter: google_requests.Request = google_requests.Request()
firebase_app: t.Any = None


class AuthSettings(AuthBaseSettings):
    api_key: SecretStr = SecretStr("")
    app_id: str = ""
    messaging_sender_id: str = ""

    @depends.inject
    def __init__(self, config: Config = depends(), **data: t.Any) -> None:
        super().__init__(**data)
        self.token_id = (
            f"_ss_{b64encode(config.app.name.encode()).decode().rstrip('=')}"
        )


class CurrentUser(AuthBaseUser):
    user_data: t.Any = {}

    def has_role(self, role: str) -> str:
        return self.user_data.custom_claims.get(role)

    def set_role(self, role: str) -> str | bool | None:
        return auth.set_custom_user_claims(self.user_data["uid"], {role: True})

    @property
    def identity(self) -> str | None:
        return self.user_data.get("uid")

    @property
    def display_name(self) -> str | None:
        return self.user_data.get("name")

    @property
    def email(self) -> EmailStr | None:
        return self.user_data.get("email")

    @property
    def gmail(self) -> str | None:
        return self.user_data.get("gmail")

    @depends.inject
    def is_authenticated(
        self, request: Request | None, config: Config = depends()
    ) -> bool | str:
        if request:
            with suppress(
                auth.ExpiredIdTokenError,
                auth.RevokedIdTokenError,
                auth.InvalidIdTokenError,
            ):
                session_cookie = request.session.get(config.auth.token_id)
                if session_cookie:
                    self.user_data = auth.verify_session_cookie(
                        session_cookie, check_revoked=True
                    )
        return self.identity or False


current_user.set(CurrentUser())


class Auth(AuthBase):
    @depends.inject
    def __init__(
        self,
        secret_key: t.Optional[SecretStr] = None,
        user_model: t.Optional[SQLModel] = None,
    ) -> None:
        self.secret_key = secret_key or self.config.app.secret_key
        self.middlewares = [
            Middleware(
                SessionMiddleware,  # type: ignore
                secret_key=self.secret_key.get_secret_value(),
                session_cookie=f"{self.config.app.name}_dash",
                https_only=True if self.config.deployed else False,
            )
        ]
        self.name = "firebase"
        self.user_model = user_model

    async def init(self) -> None:
        global firebase_app
        firebase_options: dict[str, str] = dict(projectId=self.config.app.project)
        firebase_app = initialize_app(options=firebase_options.copy())

    async def login(self, request: Request) -> bool:
        id_token = request.cookies.get(self.config.auth.token_id)
        if id_token:
            if current_user.get().is_authenticated(request):
                return True
            user_data = None
            with suppress(
                auth.ExpiredIdTokenError,
                auth.RevokedIdTokenError,
                auth.InvalidIdTokenError,
            ):
                user_data = auth.verify_id_token(id_token, check_revoked=True)
            if user_data:
                self.user_model = depends.get(import_adapter("models")).Person
                sql = depends.get(import_adapter("sql"))
                async with sql.session as session:
                    user_query = select(self.user_model).where(  # type: ignore
                        self.user_model.gmail == user_data["email"]  # type: ignore
                        and self.user_model.is_active  # type: ignore
                        and self.user_model.is_superuser  # type: ignore
                    )
                    result = await session.execute(user_query)
                    enabled_user = result.one_or_none()
                if enabled_user and (time() - user_data["auth_time"] < 5 * 6):
                    enabled_user = enabled_user[0]
                    auth.set_custom_user_claims(
                        user_data["uid"], {enabled_user.role: True}
                    )
                    enabled_user.name = (user_data["name"],)
                    enabled_user.uid = (user_data["uid"],)
                    enabled_user.image = (user_data["picture"],)
                    await enabled_user.save()
                    expires_in = timedelta(days=14)
                    session_cookie = auth.create_session_cookie(
                        id_token, expires_in=expires_in
                    )
                    self.config.auth.session_cookie = session_cookie
                    request.session.update({self.config.auth.token_id: session_cookie})
                    debug(request.session.keys())
                    return True
                else:
                    auth.revoke_refresh_tokens(user_data["uid"])
        request.session.pop(self.config.auth.token_id, None)
        current_user.get().user_data = {}
        return False

    async def logout(self, request: Request) -> bool:
        request.session.pop(self.config.auth.token_id, None)
        with suppress(
            auth.ExpiredIdTokenError,
            auth.RevokedIdTokenError,
            auth.InvalidIdTokenError,
            ValueError,
        ):
            id_token = request.cookies.get(self.config.auth.token_id)
            user_data = auth.verify_id_token(id_token, check_revoked=True)
            auth.revoke_refresh_tokens(user_data["uid"])
            current_user.get().user_data = {}
            return True
        return False

    @staticmethod
    async def authenticate(request: Request) -> bool:
        return current_user.get().is_authenticated(request)


depends.set(Auth)
