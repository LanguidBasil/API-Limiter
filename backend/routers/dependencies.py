
ALLOWED_METHODS = ["CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "POST", "PUT", "TRACE"]


def validate_method(method: str) -> str:
    method = method.upper()
    if method not in ALLOWED_METHODS:
        raise ValueError(f"method {method} is not allowed, should be one of {ALLOWED_METHODS}")
    
    return method

def validate_method_if_not_none(method: str | None = None) -> str | None:
    if method is None:
        return None
    
    return validate_method(method)
