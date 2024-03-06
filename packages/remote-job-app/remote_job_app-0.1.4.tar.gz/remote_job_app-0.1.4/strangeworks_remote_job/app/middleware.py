"""common.py."""
import json  # noqa E402
from dataclasses import dataclass

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from strangeworks_core.config.config import Config
from sw_product_lib.platform.gql import ProductAPI
from sw_product_lib.service import RequestContext

from strangeworks_remote_job.artifact import ArtifactGenerator
from strangeworks_remote_job.remote import RemoteJobAPI

from . import RemoteJobAPIClass, ResultGenerator, SubmitArtifactGen


_cfg = Config()


ignore_paths = ["/docs", "/openapi.json", "/"]


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Add RequestContext to the request."""

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)

    async def dispatch(self, request, call_next):  # noqa
        if request.url.path in ignore_paths:
            return await call_next(request)

        request.state.params = RequestParams.from_request(request)
        return await call_next(request)


# TODO: artifact generators need to be injected somehow.
artifact_generators: dict[str, ArtifactGenerator] = {
    "/jobs/submit": SubmitArtifactGen,
    "/jobs/fetch-result": ResultGenerator,
}


@dataclass
class RequestParams:
    """Class for items needed to handle a request."""

    ctx: RequestContext
    remote_api: RemoteJobAPI  # TODO: figure out how to inject this
    artifact_generator: ArtifactGenerator

    @classmethod
    def from_request(cls, request: Request) -> "RequestParams":
        ctx = RequestContext.from_request(request=request)
        ctx.api = _get_product_api()

        return cls(
            ctx=ctx,
            remote_api=RemoteJobAPIClass(),
            artifact_generator=artifact_generators.get(request.url.path),
        )


def _get_product_api(cfg: Config = _cfg) -> ProductAPI:
    return ProductAPI(
        api_key=cfg.get("api_key", profile="platform"),
        base_url=_cfg.get("api_url", "platform"),
    )
