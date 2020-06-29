from passlib.context import CryptContext
from pathlib import Path


class LoginManager:

	def __init__(self):
		self.HASHES_PATH = Path("hashes.txt")
		self.PWD_CONTEXT = CryptContext(
			schemes = ["pbkdf2_sha256"],
			default = "pbkdf2_sha256",
			pbkdf2_sha256__default_rounds = 30000
		)
		self.saved_hashes = self.get_hashes()

	def get_hashes(self):
		self.HASHES_PATH.touch()  # will create file, if it exists will do nothing
		with open(self.HASHES_PATH) as file:
			lines = []
			for line in file:
				lines.append(line.strip())
			file.close()
		return lines

	def encrypt_password(self, password):
		with open(self.HASHES_PATH, "a+") as file:
			file.write(self.PWD_CONTEXT.hash(password))

	def check_encrypted_password(self, password):
		if password is not None:
			for hashed in self.saved_hashes:
				if self.PWD_CONTEXT.verify(password, hashed):
					return True
		return False
