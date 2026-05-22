from flask import request, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

EXEMPT_ROUTES = [
    "/api/auth/signup",
    "/api/auth/login",
    "/api/verify",
    "/health",
    "/",
    "/login",
    "/signup",
    "/verify",
    "/dashboard",
    "/reports",
    "/profile",
    "/static/",
]

def jwt_middleware():
    if request.path in EXEMPT_ROUTES or request.method == "OPTIONS":
        return
    if request.path.startswith("/static/"):
        return

    try:
        if request.path.startswith("/api/"):
            verify_jwt_in_request()
            g.current_user = get_jwt_identity()
    except Exception:
        pass

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        g.current_user = get_jwt_identity()
        return fn(*args, **kwargs)
    return wrapper
