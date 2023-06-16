from fastapi import APIRouter


router = APIRouter(prefix="/validate")


@router.post("/", response_model=bool)
def validate(validate: str, method: str, ip_address: str):
    """Return if new request is allowed. Specify seconds to refresh in header"""
    pass
