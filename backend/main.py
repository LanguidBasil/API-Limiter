from pathlib import Path
from pkgutil import iter_modules
from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app_v1 = FastAPI(title="API Limiter", version="1.0", docs_url=None, redoc_url=None)
app_v1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


package_dir = Path(__file__).resolve().parent / "routers"
for _, module_name, is_pkg in iter_modules([str(package_dir)]):
    if not is_pkg:
        continue
    app_v1.include_router(
        import_module(f"{__package__}.routers.{module_name}.router").router,
        tags=[module_name],
    )


app = FastAPI()
app.mount("/v1", app_v1)
