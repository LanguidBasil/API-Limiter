

def method_to_upper_if_not_none(method: str | None = None) -> str | None:
    return method.upper() if method is not None else None
