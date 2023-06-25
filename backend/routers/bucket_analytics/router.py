from datetime import datetime
from csv import writer
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from .schemas import BucketFilter_Body
from ..dependencies import make_dependable
from ...database import bucket_analytics_storage, BucketAnalytics


router = APIRouter(prefix="/bucket_analytics")


@router.get(
    "/data/csv", 
    response_class=StreamingResponse,
    responses={
        200: {
            "content": { "text/csv": {} },
        },
    },
)
def get_csv(body: BucketFilter_Body = Depends(make_dependable(BucketFilter_Body))):
    with StringIO() as buffer:
        csv_writer = writer(buffer)
        
        # didn't found a way to get values of dataclass as list, hence the unfortunate duplication
        # at least it's robust =D
        csv_writer.writerow(["url", "method", "ip_address", "timestamp", "was_allowed"])
        csv_writer.writerows([
            [
                bucket.url, 
                bucket.method, 
                bucket.ip_address, 
                datetime.fromtimestamp(bucket.timestamp), 
                bucket.was_allowed
            ]
            for bucket
            in bucket_analytics_storage.get(body.url, body.method, body.ip_address)
        ])
        
        buffer.seek(0)
        return StreamingResponse(
            iter(buffer.read()), 
            media_type="text/csv", 
            headers={ "Content-Disposition": "attachment; filename=data.csv" }
        )
        
@router.get("/data/json", response_model=list[BucketAnalytics])
def get_json(body: BucketFilter_Body = Depends(make_dependable(BucketFilter_Body))):
    return bucket_analytics_storage.get(body.url, body.method, body.ip_address)
