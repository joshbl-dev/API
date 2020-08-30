import os

from flask import Flask, redirect, request

from Scheduler import schedule_tasks
from accounts.LoginManager import LoginManager
import redirects

SECURE_ENDPOINTS = ["/startPC"]
ADMIN_ENDPOINTS = ["/register", "/deluser"]

app = Flask(__name__)
login_manager = LoginManager()

scheduler = schedule_tasks()


@app.route('/startPC', methods=['GET'])
def start_pc():
    os.system("sudo etherwake -i eth0 00:4E:01:C1:FF:53")
    return "Successful!"


@app.route('/', methods=['GET'])
def home():
    return redirect(redirects.REDIRECT_URL)


@app.route('/register', methods=['GET'])
def register():
    username = request.headers.get("newusername")
    if username is not None:
        return login_manager.create_account(username)
    else:
        return "<h1>Ensure header contains {newusername}</h1>"


@app.route('/deluser', methods=['GET'])
def deluser():
    username = request.headers.get("deluser")
    if username is not None:
        return login_manager.delete_account(username)
    else:
        return "<h1>Ensure header contains {username}</h1>"


@app.before_request
def before_request():
    path = request.path
    password = request.headers.get("password")
    username = request.headers.get("username")

    if username is not None and password is not None:
        if not (login_manager.is_admin(username) and login_manager.validate_request(ADMIN_ENDPOINTS, path,
                                                                                    login_manager.ADMIN_USERNAME,
                                                                                    password)) and not login_manager.validate_request(
            SECURE_ENDPOINTS, path,
            username, password):
            return redirect(redirects.rejected_perms())
    else:
        return redirect(redirects.invalid_request())


if __name__ == '__main__':
    app.run(debug=True, port=80)
