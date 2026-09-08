from app.models.user import User
from app.auth.security import hash_password

users = []


def create_user(name: str, email: str, password: str):
    user_id = len(users) + 1

    hashed_password = hash_password(password)

    new_user = User(
        user_id=user_id,
        name=name,
        email=email,
        password=hashed_password
    )

    users.append(new_user)

    return new_user


def get_all_users():
    return users


def get_user_by_id(user_id: int):
    for user in users:
        if user.id == user_id:
            return user

    return None
def get_user_by_email(email: str):
    for user in users:
        if user.email == email:
            return user

    return None


def update_user(user_id: int, name: str, email: str):
    for user in users:
        if user.id == user_id:
            user.name = name
            user.email = email
            return user

    return None


def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user

    return None