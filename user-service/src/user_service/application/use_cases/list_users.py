from user_service.domain.entities.user import User
from user_service.domain.repositories.user_repository import UserRepository


class ListUsers:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, limit: int = 50, offset: int = 0) -> list[User]:
        return self.user_repository.list(limit=limit, offset=offset)
