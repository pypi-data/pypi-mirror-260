class Config:
	def __init__(self, encoding: str = "UTF-8", 
					use_rich_print: bool = True, encode_bool:bool = False,
					md5_solt: str = "solt") -> None:
		"""Basic configuration for data encoding and decoding

		:param str encoding: The encoding into which the data will be encoded. Default ascii. Can be: utf-8
		:param str use_rich_print: Use print from the rich library instead of typical raise errors
		:param str encode_bool: Encode logical values by type False, True. No by default
		:param str md5_solt: Add a "salt" for encrypting data in md5
		"""
		self._encoding = encoding
		self._use_print = use_rich_print
		self._encode_bool = encode_bool
		self._md5_solt = md5_solt