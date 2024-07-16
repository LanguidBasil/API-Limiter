from dataclasses import dataclass
from redis import Redis

from ..utils import HTTPMethod


@dataclass(slots=True)
class Bucket:
    url: str
    method: HTTPMethod
    ip_address: str

    requests_left: int | None = None
    first_request_timestamp: float | None = None


class BucketStorage:
    __connection: Redis

    def __init__(self, connection: Redis) -> None:
        self.__connection = connection

    def save(self, bucket: Bucket) -> None:
        if bucket.requests_left is None:
            raise ValueError(f"requests_left is empty on bucket {bucket}, which is not allowed on saving")
        if bucket.first_request_timestamp is None:
            raise ValueError(f"first_request_timestamp is empty on bucket {bucket}, which is not allowed on saving")

        self.__connection.hset(
            f"buckets#{bucket.url}#{bucket.method.value}#{bucket.ip_address}",
            mapping={
                "requests_left": bucket.requests_left,
                "first_request_timestamp": bucket.first_request_timestamp,
            },
        )

    def get(self, bucket: Bucket) -> Bucket | None:
        redis_bucket = self.__connection.hgetall(f"buckets#{bucket.url}#{bucket.method.value}#{bucket.ip_address}")
        if not redis_bucket:
            return None

        return Bucket(
            url=bucket.url,
            method=bucket.method,
            ip_address=bucket.ip_address,
            requests_left=int(redis_bucket["requests_left"]),
            first_request_timestamp=float(redis_bucket["first_request_timestamp"]),
        )
