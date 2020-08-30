import json
import os
import random
import string
from pathlib import Path

from passlib.context import CryptContext

import redirects

PASSWORD_VALUES = list(f'{string.ascii_letters} + {string.digits}')


def update_json(file):
    file.flush()
    os.fsync(file.fileno())


def create_password():
    random.shuffle(PASSWORD_VALUES)
    return ''.join(random.choices(PASSWORD_VALUES, k=12))


class LoginManager:

    def __new__(cls):
        return super().__new__(cls)

    def __init__(self):
        self.ACCOUNTS_PATH = Path("accounts.json")
        self.ADMIN_USERNAME = "joshbl"
        self.PWD_CONTEXT = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000
        )
        self.check_json()
        self.saved_accounts = self.get_accounts()

    def validate_request(self, endpoint, path, username, password):
        return endpoint.__contains__(path) and self.check_encrypted_password(username, password)

    def check_json(self):
        if not self.ACCOUNTS_PATH.exists():
            with open(self.ACCOUNTS_PATH, "w") as file:
                file.write(json.dumps({}))
                update_json(file)
                file.close()

    def save_json(self):
        with open(self.ACCOUNTS_PATH, "w") as json_file:
            json_file.write(json.dumps(self.saved_accounts))
            update_json(json_file)
            json_file.close()

    def get_accounts(self):
        with open(self.ACCOUNTS_PATH) as hashes_json:
            accounts = json.load(hashes_json)
            hashes_json.close()
            print(accounts)
        return accounts

    def create_account(self, username):
        if not self.saved_accounts.__contains__(username):
            password = create_password()
            password_hash = self.PWD_CONTEXT.hash(password)
            self.saved_accounts.update({username: password_hash})
            self.save_json()
            return "<h1>Account creation successful!</h1>" + "<p>Username: " + username + "\nPassword: " + password + "</p> "
        return "<h1>Account username {" + username + "} already exists!</h1>"

    def delete_account(self, username):
        if self.is_admin(username):
            return redirects.rejected_perms()
        else:
            self.saved_accounts.pop(username)
            self.save_json()
            return "<h1>Account username {" + username + "} deleted.</h1>"

    def is_admin(self, username):
        return username == self.ADMIN_USERNAME

    def check_encrypted_password(self, username, password):
        try:
            account_hash = self.saved_accounts[username]
        except KeyError:
            return False
        return username is not None and password is not None and account_hash is not None and self.PWD_CONTEXT.verify(
            password, account_hash)
