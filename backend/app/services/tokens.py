from cryptography.fernet import Fernet

from app.core.config import settings


class TokenCipher:
    def __init__(self) -> None:
        self._fernet = Fernet(settings.encryption_key.encode())

    def encrypt(self, token: str) -> str:
        return self._fernet.encrypt(token.encode()).decode()

    def decrypt(self, encrypted_token: str) -> str:
        return self._fernet.decrypt(encrypted_token.encode()).decode()
