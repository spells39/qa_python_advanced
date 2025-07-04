from app.models.models import User
from config import Server
from utils.base_session import BaseSession


class ServiceModel:
    def __init__(self, env):
        self.session = BaseSession(base_url=Server(env).service)

    def get_user(self, user_id: int):
        return self.session.get(f"users/{user_id}")

    def create_user(self, user: User):
        return self.session.post("users/", json=user)

    def delete_user(self, user_id: int):
        return self.session.delete(f"users/{user_id}")

    def get_users(self):
        return self.session.get("users/")

    def update_user(self, user_id: int, user: User):
        return self.session.patch(f"users/{user_id}", json=user)

    def check_status(self):
        return self.session.get("check_status")