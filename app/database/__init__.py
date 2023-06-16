from redis import Redis
from .rule import Rule, RuleStorage
from .bucket import Bucket, BucketStorage


connection = Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

ruleStorage = RuleStorage(connection)
bucketStorage = BucketStorage(connection)

__all__ = [
    "Rule",
    "ruleStorage",
    "bucketStorage",
    "Bucket",
]

