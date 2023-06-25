from pydantic import BaseModel, HttpUrl, IPvAnyAddress
from ...utils import HTTPMethod


class BucketFilter_Body(BaseModel):
    url: HttpUrl | None = None
    method: HTTPMethod | None = None
    ip_address: IPvAnyAddress | None = None
