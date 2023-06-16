from redis import Redis
from .rule import Rule, RuleStorage
from .bucket import Bucket, BucketStorage


connection = Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

rule_storage = RuleStorage(connection)
bucket_storage = BucketStorage(connection)

__all__ = [
    "Rule",
    "rule_storage",
    "bucket_storage",
    "Bucket",
]

