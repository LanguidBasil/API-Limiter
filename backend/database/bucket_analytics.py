from dataclasses import dataclass
from redis import Redis

from ..utils import HTTPMethod

    
@dataclass(slots=True)
class BucketAnalytics:
    url: str
    method: HTTPMethod
    ip_address: str
    timestamp: float
    
    was_allowed: bool

class BucketAnalyticsStorage:
    __connection: Redis
    
    def __init__(self, connection: Redis) -> None:
        self.__connection = connection
    
    def save(self, bucket: BucketAnalytics) -> None:        
        self.__connection.hset(
            f"bucketsanalytics#{bucket.url}#{bucket.method.value}#{bucket.ip_address}#{bucket.timestamp}",
            mapping={
                "was_allowed": bucket.was_allowed,
            },
        )
    
    def get(
            self, 
            url: str = None, 
            method: HTTPMethod = None, 
            ip_address: str = None
        ) -> list[BucketAnalytics]:
        
        pattern = "bucketsanalytics"
        pattern += f"#{url if url is not None else '*'}"
        pattern += f"#{method.value if method is not None else '*'}"
        pattern += f"#{ip_address if ip_address is not None else '*'}"
        pattern += "#*"
        keys: list[str] = self.__connection.keys(pattern)
        
        buckets = []
        for key in keys:
            redis_bucket = self.__connection.hgetall(key)
            
            key = key.split("#")
            url, method, ip_address, timestamp = key[1], HTTPMethod(key[2]), key[3], float(key[4])
            
            buckets.append(BucketAnalytics(
                url=url,
                method=method,
                ip_address=ip_address,
                timestamp=timestamp,
                was_allowed=bool(redis_bucket["was_allowed"]),
            ))
        
        return buckets
