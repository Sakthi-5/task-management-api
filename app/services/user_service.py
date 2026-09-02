from app.models.user import User

users = []


def create_user(name: str, email: str):
    user_id = len(users) + 1

    new_user = User(
        user_id=user_id,
        name=name,
        email=email
    )

    users.append(new_user)

    return new_user
def get_all_users():
    return users