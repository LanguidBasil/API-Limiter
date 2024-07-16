from fastapi import APIRouter, Depends
from ..schemas import Bucket_Body
from ..dependencies import make_dependable
from ...database import bucket_storage, Bucket


router = APIRouter(prefix="/buckets")


@router.get("/", response_model=Bucket | None)
def get_bucket(body: Bucket_Body = Depends(make_dependable(Bucket_Body))):
    return bucket_storage.get(
        Bucket(
            url=body.url,
            method=body.method,
            ip_address=str(body.ip_address),
        )
    )
