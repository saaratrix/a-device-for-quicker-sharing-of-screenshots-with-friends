from werkzeug.security import generate_password_hash, check_password_hash


def generate_hash(password: str) -> str:
    return generate_password_hash(password)


def check_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)

