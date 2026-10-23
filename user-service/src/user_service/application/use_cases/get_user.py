from uuid import UUID

from user_service.domain.entities.user import User
from user_service.domain.exceptions import UserNotFoundError
from user_service.domain.repositories.user_repository import UserRepository


class GetUser:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: UUID) -> User:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user
