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
        
        if url is not None and method is not None and ip_address is None:
            redis_bucket = self.__connection.hgetall(
                f"bucketsanalytics#{url}#{method.value}#{ip_address}#*"
            )
            if not redis_bucket:
                return []
            
            return [BucketAnalytics(
                url=url,
                method=method,
                ip_address=ip_address,
                was_allowed=bool(redis_bucket["was_allowed"]),
                timestamp=float(redis_bucket["timestamp"]),
            )]
        
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
            url, method, ip_address = key[1], HTTPMethod(key[2]), key[3]
            
            buckets.append(BucketAnalytics(
                url=url,
                method=method,
                ip_address=ip_address,
                was_allowed=bool(redis_bucket["was_allowed"]),
                timestamp=float(redis_bucket["timestamp"]),
            ))
        
        return buckets
