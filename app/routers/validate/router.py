from datetime import datetime

from fastapi import APIRouter, Depends

from .schemas import Validate_Response
from ..dependencies import method_to_upper_if_not_none
from ...database import bucket_storage, Bucket, rule_storage


router = APIRouter(prefix="/validate")


@router.post("/", response_model=Validate_Response)
def validate(ip_address: str, url: str, method: str = Depends(method_to_upper_if_not_none)):
    
    rule = rule_storage.get(url, method)[0]
    if not rule:
        return Validate_Response(
            is_allowed=True,
            requests_left=None,
            seconds_to_next_refresh=None,
        )
    
    
    bucket = Bucket(
        url=url,
        method=method,
        ip_address=ip_address,
        
        requests_left=None,
        first_request_timestamp=None,
    )
    
    redis_bucket = bucket_storage.get(bucket)
    now = datetime.now().timestamp()
    
    
    if (
            not redis_bucket or 
            redis_bucket.first_request_timestamp + rule.refresh_rate < now
        ):
        
        bucket.requests_left = rule.requests - 1
        bucket.first_request_timestamp = now
        bucket_storage.save(bucket)
        return Validate_Response(
            is_allowed=True,
            requests_left=bucket.requests_left,
            seconds_to_next_refresh=rule.refresh_rate,
        )
    
    
    seconds_to_next_refresh = rule.refresh_rate - (now - redis_bucket.first_request_timestamp)
        
    if redis_bucket.requests_left < 1:
        return Validate_Response(
            is_allowed=False,
            requests_left=0,
            seconds_to_next_refresh=seconds_to_next_refresh,
        )
    
    bucket.requests_left = redis_bucket.requests_left - 1
    bucket.first_request_timestamp = redis_bucket.first_request_timestamp
    bucket_storage.save(bucket)
    return Validate_Response(
        is_allowed=True,
        requests_left=bucket.requests_left,
        seconds_to_next_refresh=seconds_to_next_refresh,
    )
