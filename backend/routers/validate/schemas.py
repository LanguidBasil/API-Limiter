from pydantic import BaseModel


class Validate_Response(BaseModel):
    is_allowed: bool
    requests_left: int | None
    seconds_to_next_refresh: float | None

