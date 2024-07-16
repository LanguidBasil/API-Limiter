from redis import Redis
from .rule import Rule, RuleStorage
from .bucket import Bucket, BucketStorage
from .bucket_analytics import BucketAnalytics, BucketAnalyticsStorage


connection = Redis(
    host="redis",
    port=6379,
    decode_responses=True,
)

rule_storage = RuleStorage(connection)
bucket_storage = BucketStorage(connection)
bucket_analytics_storage = BucketAnalyticsStorage(connection)

__all__ = [
    "Rule",
    "rule_storage",
    "Bucket",
    "bucket_storage",
    "BucketAnalytics",
    "bucket_analytics_storage",
]
