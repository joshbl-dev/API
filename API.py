import os

from flask import Flask, redirect, request

from accounts.LoginManager import LoginManager

SECURE_ENDPOINTS = ["/startPC"]
ADMIN_ENDPOINTS = ["/register", "/deluser"]
REDIRECT_URL = "https://joshbl.dev"

app = Flask(__name__)
login_manager = LoginManager()


@app.route('/startPC', methods = ['GET'])
def start_pc():
	os.system("sudo etherwake -i eth0 00:4E:01:C1:FF:53")
	return "Successful!"


@app.route('/', methods = ['GET'])
def home():
	return redirect(REDIRECT_URL)


@app.route('/register', methods = ['GET'])
def register():
	username = request.args.get("newusername")
	if username is not None:
		return login_manager.create_account(username)
	else:
		return "<h1>Ensure header contains {username}</h1>"


@app.route('/deluser', methods = ['GET'])
def deluser():
	username = request.args.get("deluser")
	if username is not None:
		return login_manager.delete_account(username)
	else:
		return "<h1>Ensure header contains {username}</h1>"


@app.before_request
def before_request():
	path = request.path
	password = request.args.get("password")
	username = request.args.get("username")

	if username is not None and password is not None:
		if not (login_manager.is_admin(username) and login_manager.validate_request(ADMIN_ENDPOINTS, path,
				login_manager.ADMIN_USERNAME, password)) and not login_manager.validate_request(SECURE_ENDPOINTS, path,
				username, password):
			return redirect(REDIRECT_URL + "/403")
	else:
		return redirect(REDIRECT_URL + "/404")


if __name__ == '__main__':
	app.run(debug = True, port = 80)
