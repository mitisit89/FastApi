from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from starlette.requests import Request

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH

bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/login")

SECRET = SECRET_AUTH


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def get_enabled_backends(request: Request):
    """Return the enabled dependencies following custom logic."""
    return [auth_backend]

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
