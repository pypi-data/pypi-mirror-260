from typing import Optional
import keyring
import keyring.errors


Exception = keyring.errors.KeyringError


def get_saved_password(email: str) -> Optional[str]:
    return keyring.get_password("Bullseye", email)


def save_password(email: str, password: str):
    keyring.set_password("Bullseye", email, password)
