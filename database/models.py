from typing import Optional, Union
from beanie import Document
from motor.core import pymongo


class Request(Document):
    method: str
    url: str
    headers: dict
    cookie: Optional[Union[dict, str]] = {}
    payload: Optional[Union[dict, str]] = {}

    class Settings:
        name = "requests"
        indexes = [
            [("method", pymongo.ASCENDING), ("url", pymongo.ASCENDING)],
        ]
