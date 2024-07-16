from datetime import datetime

from fastapi import APIRouter, Depends


from .schemas import Validate_Response
from ..schemas import Bucket_Body
from ..dependencies import make_dependable
from ...database import (
    bucket_storage,
    Bucket,
    rule_storage,
    bucket_analytics_storage,
    BucketAnalytics,
)


def __validate__return_and_save_bucket(body: Bucket_Body, response: Validate_Response) -> Validate_Response:
    bucket_analytics_storage.save(
        BucketAnalytics(
            url=body.url,
            method=body.method,
            ip_address=body.ip_address,
            was_allowed=str(response.is_allowed),
            timestamp=datetime.now().timestamp(),
        )
    )
    return response


router = APIRouter(prefix="/validate")


@router.post("/", response_model=Validate_Response)
def validate(body: Bucket_Body = Depends(make_dependable(Bucket_Body))):
    rules = rule_storage.get(body.url, body.method)
    if not rules or not (rule := rules[0]):
        return __validate__return_and_save_bucket(
            body,
            Validate_Response(
                is_allowed=True,
                requests_left=None,
                seconds_to_next_refresh=None,
            ),
        )

    bucket = Bucket(
        url=body.url,
        method=body.method,
        ip_address=body.ip_address,
        requests_left=None,
        first_request_timestamp=None,
    )

    redis_bucket = bucket_storage.get(bucket)
    now = datetime.now().timestamp()

    if not redis_bucket or redis_bucket.first_request_timestamp + rule.refresh_rate < now:
        bucket.requests_left = rule.requests - 1
        bucket.first_request_timestamp = now
        bucket_storage.save(bucket)
        return __validate__return_and_save_bucket(
            body,
            Validate_Response(
                is_allowed=True,
                requests_left=bucket.requests_left,
                seconds_to_next_refresh=rule.refresh_rate,
            ),
        )

    seconds_to_next_refresh = rule.refresh_rate - (now - redis_bucket.first_request_timestamp)

    if redis_bucket.requests_left < 1:
        return __validate__return_and_save_bucket(
            body,
            Validate_Response(
                is_allowed=False,
                requests_left=0,
                seconds_to_next_refresh=seconds_to_next_refresh,
            ),
        )

    bucket.requests_left = redis_bucket.requests_left - 1
    bucket.first_request_timestamp = redis_bucket.first_request_timestamp
    bucket_storage.save(bucket)
    return __validate__return_and_save_bucket(
        body,
        Validate_Response(
            is_allowed=True,
            requests_left=bucket.requests_left,
            seconds_to_next_refresh=seconds_to_next_refresh,
        ),
    )
