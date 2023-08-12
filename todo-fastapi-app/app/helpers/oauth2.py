from app.db.fake_users_db import fake_users_db
from app.gateways.users_gateway import get_user


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password
