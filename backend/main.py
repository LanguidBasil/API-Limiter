from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.rules.router import router as rules_router
from .routers.validate.router import router as validate_router


app = FastAPI(title="API Limiter", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rules_router,    tags=["Rules"])
app.include_router(validate_router, tags=["Validation"])
