import os
from flask_httpauth import HTTPBasicAuth
from ..utility.password_utility import generate_hash, check_password

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username: str, password: str) -> bool:
    valid_user = AdminCredentials.check_admin_username(username)
    return valid_user and AdminCredentials.check_admin_password(password)


class AdminCredentials:
    __admin_username = os.environ.get('ADMIN_USERNAME', 'SECRET')
    __admin_password = os.environ.get('ADMIN_PASSWORD', 'SECRET')
    __admin_password_hash = generate_hash(__admin_password)

    @staticmethod
    def check_admin_username(username: str) -> bool:
        return username == AdminCredentials.__admin_username

    @staticmethod
    def check_admin_password(password: str) -> bool:
        if AdminCredentials.__admin_password is 'SECRET':
            return False

        return check_password(password, AdminCredentials.__admin_password_hash)


