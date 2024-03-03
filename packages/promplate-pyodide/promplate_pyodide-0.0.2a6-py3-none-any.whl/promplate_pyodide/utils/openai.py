from contextlib import suppress
from functools import cache
from typing import cast

from pyodide.code import run_js
from pyodide.ffi import JsCallable, register_js_module, to_js

from .. import patch_httpx, patch_openai, patch_promplate


async def ensure_openai(fallback_import_url: str = "https://esm.run/openai"):
    with suppress(ModuleNotFoundError):
        import openai

    openai = await run_js(  # noqa
        "(async () => ({ __all__: [], ...await import('openai'), version: await import('openai/version') }))()".replace(
            "openai", fallback_import_url
        )
    )

    register_js_module("openai", openai)


@cache
def translate_openai():
    from openai import OpenAI

    js_openai_class = cast(JsCallable, OpenAI)

    def make_client(
        api_key: str | None = None,
        organization: str | None = None,
        base_url: str | None = None,
        timeout: float | None = None,
        max_retries: int | None = None,
        default_headers: dict | None = None,
        default_query: dict | None = None,
        **_,
    ):
        return js_openai_class.new(
            apiKey=api_key or "",
            organization=organization,
            baseURL=base_url,
            timeout=timeout,
            maxRetries=max_retries,
            defaultHeaders=to_js(default_headers),
            defaultQuery=to_js(default_query),
            dangerouslyAllowBrowser=True,
        )

    return make_client


async def patch_all():
    await patch_openai()
    patch_httpx()
    patch_promplate(True)
