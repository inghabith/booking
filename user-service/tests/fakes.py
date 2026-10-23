"""Adaptador en memoria: prueba los casos de uso sin base de datos."""
from user_service.domain.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def add(self, user):
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def get_by_email(self, email):
        return next((u for u in self.users.values() if u.email == email.lower()), None)

    def get_by_identification(self, identification_type, identification_number):
        return next(
            (
                u
                for u in self.users.values()
                if u.identification_type == identification_type
                and u.identification_number == identification_number
            ),
            None,
        )

    def list(self, limit=50, offset=0):
        return list(self.users.values())[offset : offset + limit]
