from dataclasses import dataclass
from redis import Redis


@dataclass(slots=True)
class Bucket:
    url: str
    method: str
    ip_address: str
    
    requests_left: int
    first_request_timestamp: float

class BucketStorage:
    __connection: Redis
    
    def __init__(self, connection: Redis) -> None:
        self.__connection = connection
    
    
    def save(bucket: Bucket) -> None:
        pass
    
    def get(url: str, method: str, ip_address) -> Bucket | None:
        pass
