from flask import Flask, redirect, request
import os
from passlib.context import CryptContext
from pathlib import Path

HASHES_PATH = Path("hashes.txt")
SECURE_ENDPOINTS = ["/startPC"]
REDIRECT_URL = "https://joshbl.dev"

app = Flask(__name__)

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def get_hashes():
    HASHES_PATH.touch()  # will create file, if it exists will do nothing
    with open(HASHES_PATH) as file:
        lines = []
        for line in file:
            lines.append(line.strip())
        print(lines)
        file.close()
    return lines


def encrypt_password(password):
    with open(HASHES_PATH, "a+") as file:
        file.write(pwd_context.hash(password))


def check_encrypted_password(password):
    if password is not None:
        for hashed in get_hashes():
            if pwd_context.verify(password, hashed):
                return True
    return False


@app.route('/startPC', methods=['GET'])
def start_pc():
    os.system("sudo etherwake -i eth0 00:4E:01:C1:FF:53")
    return "Successful!"


@app.route('/', methods=['GET'])
def home():
    return redirect(REDIRECT_URL)


@app.before_request
def before_request():
    if SECURE_ENDPOINTS.__contains__(request.path) and not check_encrypted_password(request.args.get("password")):
        return redirect(REDIRECT_URL + "/403")


if __name__ == '__main__':
    app.run(debug=True,port=80)