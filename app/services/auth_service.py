from app.services.user_service import get_user_by_email
from app.auth.security import verify_password
def authenticate_user(email: str, password: str):
    user = get_user_by_email(email)

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user