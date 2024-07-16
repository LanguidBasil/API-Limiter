from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.rules.router import router as rules_router
from .routers.buckets.router import router as buckets_router
from .routers.validate.router import router as validate_router
from .routers.bucket_analytics.router import router as bucket_analytics_router


app_v1 = FastAPI(title="API Limiter", version="1.0", docs_url=None, redoc_url=None)
app_v1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_v1.include_router(rules_router, tags=["Rules"])
app_v1.include_router(buckets_router, tags=["Buckets"])
app_v1.include_router(validate_router, tags=["Validation"])
app_v1.include_router(bucket_analytics_router, tags=["Bucket analytics"])


app = FastAPI()
app.mount("/v1", app_v1)
