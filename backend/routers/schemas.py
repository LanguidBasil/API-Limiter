from pydantic import BaseModel, HttpUrl, IPvAnyAddress
from ..utils import HTTPMethod


class Bucket_Body(BaseModel):
    url: HttpUrl
    method: HTTPMethod
    ip_address: IPvAnyAddress
