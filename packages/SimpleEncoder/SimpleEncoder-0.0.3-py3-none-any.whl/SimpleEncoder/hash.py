import hashlib as HL

from .config import Config
from .encode import Encode
from .decode import Decode

class Hash:
	def __init__(self, config: Config = Config()) -> None:
		"""Encrypt the data.
			
			Keyword arguments:
				• config -- encode Configuration. Default: Standart config.
		"""
		self.config = config
	
	def md5(self, string: str) -> str:
		"""Keyword arguments:
				• string -- String for hashing in md5. Required!

			returns a hashed string
		"""
		return HL.md5(str(string + self.config._md5_solt).encode(self.config._encoding)).hexdigest()

	def password(self, string: str) -> str:
		"""Keyword arguments:
				• string -- String for hashing in md5. Required!

			returns a hashed string
		"""
		return HL.md5(Encode(string, self.config).b64_str().encode()).hexdigest()

	def password_equals(self, password: str, string: str) -> bool:
		"""Check hashed strings for identity.
				Keyword arguments:
				• password -- A hashed string. Required!
				• string -- String for hashing in md5. Required!

			returns a boolean value
		"""
		psw = self.password(string)

		if psw == password or password == psw:
			return True
		return False