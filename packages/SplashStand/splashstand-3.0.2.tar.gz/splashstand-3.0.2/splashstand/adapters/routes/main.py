import typing as t

from acb.adapters import import_adapter
from acb.debug import debug
from acb.depends import depends
from asgi_htmx import HtmxRequest
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route
from starlette.routing import Router
from starlette.responses import Response
from starlette_async_jinja import AsyncJinja2Templates
from ._base import RoutesBase
from ._base import RoutesBaseSettings

Templates = import_adapter()


class RoutesSettings(RoutesBaseSettings): ...


class Index(HTTPEndpoint):
    templates: Templates = depends()  # type: ignore

    async def get(self, request: HtmxRequest) -> Response:
        request.path_params["page"] = request.scope["path"].lstrip("/") or "home"
        debug(request.path_params.get("page"))
        return await self.templates.app.render_template(
            request, "index.html"  # type: ignore
        )


class Block(HTTPEndpoint):
    templates: Templates = depends()  # type: ignore

    async def get(self, request: HtmxRequest) -> Response:
        debug(request)
        block = f"blocks/{request.path_params['block']}.html"
        return await self.templates.app.render_template(request, block)


class Routes(RoutesBase):
    templates: t.Optional[AsyncJinja2Templates] = None
    routes: list[Route | Router] = []

    @staticmethod
    async def favicon(request: HtmxRequest) -> Response:
        return PlainTextResponse("", 200)

    @depends.inject
    async def init(self, templates: Templates = depends()) -> None:  # type: ignore
        self.templates = templates.app
        self.routes.extend(
            [
                Route("/favicon.ico", endpoint=self.favicon, methods=["GET"]),
                Route("/", Index, methods=["GET"]),
                Route("/block/{block}", Block, methods=["GET"]),
            ]
        )
        async for page in self.templates.env.loader.searchpath[-1].glob("*.html"):
            self.routes.append(Route(f"/{page.stem}", Index, methods=["GET"]))


depends.set(Routes)
