from litestar import Litestar, get, post
from pathlib import Path
from typing import Annotated
from dataclasses import dataclass

from litestar import Litestar
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.response import Template
from litestar.enums import RequestEncodingType
from litestar.params import Body

from yt_dlp import YoutubeDL
import json


@dataclass
class DownloadData:
    url: str


@get("/")
async def index() -> Template:
    return Template("index.html")


@post("/download")
async def download(
    data: Annotated[DownloadData, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> Template:
    # FIXME: change the url
    data.url = "https://www.youtube.com/watch?v=PlvMGpQnqOM"

    with YoutubeDL() as ydl:
        info = ydl.extract_info(data.url, download=False)
        info_json = json.dumps(ydl.sanitize_info(info))

    return Template("download.html", context={"data": data, "info": info_json})


app = Litestar(
    route_handlers=[index, download],
    template_config=TemplateConfig(
        directory=Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)