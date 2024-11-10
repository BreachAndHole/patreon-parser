from typing import NamedTuple


class ParsedPostData(NamedTuple):
    id: int
    title: str
    url: str
    youtube_url: str
