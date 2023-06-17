from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.rules.router import router as rules_router
from .routers.validate.router import router as validate_router


app_v1 = FastAPI(title="API Limiter", version="1.0")
app_v1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_v1.include_router(rules_router,    tags=["Rules"])
app_v1.include_router(validate_router, tags=["Validation"])


app = FastAPI()
app.mount("/v1", app_v1)

