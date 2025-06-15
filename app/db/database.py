from typing import Dict, Optional
from app.core.security import get_password_hash
from app.models.user import UserInDB


class FakeUserDatabase:
    def __init__(self):
        self._users: Dict[str, Dict] = {
            "johndoe": {
                "username": "johndoe",
                "full_name": "John Doe",
                "email": "johndoe@example.com",
                "hashed_password": get_password_hash("kskjh892jkjfd"),
                "disabled": False,
            }
        }

    def get_user(self, username: str) -> Optional[UserInDB]:
        if username in self._users:
            user_dict = self._users[username]
            return UserInDB(**user_dict)
        return None

    def add_user(self, username: str, user_data: Dict) -> None:
        self._users[username] = user_data

    def user_exists(self, username: str) -> bool:
        return username in self._users


fake_users_db = FakeUserDatabase()
