from komodo.framework.komodo_user import KomodoUser
from komodo.store.user_store import UserStore


class UserLoader:
    @classmethod
    def load(cls, email) -> KomodoUser:
        if email == "ryan@komodoapp.ai":
            return KomodoUser(name="Ryan Oberoi", email=email)

        if email == "ram@komodoapp.ai":
            return KomodoUser(name="Ramasamy Ramar", email=email)

        if email == "test@example.com":
            return KomodoUser(name="Test User", email=email)

        user = UserStore().retrieve_user(email)
        print(user)
        return KomodoUser(name=user.name, email=user.email)
