class Validator:
	def __init__(self, data: any, use_print: bool) -> None:
		self.__data = data
		self.__use_print = use_print

	def check(self, _type: any, this: any = None) -> bool:
		data = self.__data
		if this: data = this
		if not isinstance(data, _type):
			if self.__use_print:
				from rich import print
				return print(f"[red bold][!] Error[/red bold] SimpleEncoder: Encoding data type is not a {_type}!")
			raise TypeError(f"[!] Error: SimpleEncoder: Encoding data type is not a {_type}!")
		return True

	def isBoolean(self, this: str) -> bool:
		if	isinstance(this, bool):
			return True
		return False