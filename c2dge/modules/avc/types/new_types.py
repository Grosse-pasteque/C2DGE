import os
import re
from .. import errors, types



class File:
	def __init__(self, extension=""):
		self.extension = extension


	def check(self, file, arg='file'):
		if not os.path.exists(file):
			raise FileNotFoundError(
				f"[Errno 2] No such file or directory: {repr(file)}")

		if not file.endswith(self.extension):
			raise errors.IncorrectFileExtensionError(
				f'extension of file {file!r} is icorrect for arg {arg!r}')


	def __str__(self):
		return types.str_of(self)



class Class:
	def __init__(self, regexp=r"<class '([\w_\.]*)'>"):
		self.regexp = regexp


	def check(self, _class, arg='arg'):
		if not re.match(self.regexp, str(_class)):
			types.type_error(arg, self)


	def __str__(self):
		return types.str_of(self)



class Module:
	def __init__(self):
		pass


	def check(self, module, arg='arg'):
		if str(type(module)) != "<class 'module'>":
			types.type_error(arg, self)


	def __str__(self):
		return types.str_of(self)



class Function:
	def __init__(self):
		pass


	def check(self, function, arg='arg'):
		if str(type(function)) not in ["<class 'function'>", "<class 'method'>"]:
			types.type_error(arg, self)


	def __str__(self):
		return types.str_of(self)



class Union:
	def __init__(self, *types):
		self.types = types


	def check(self, variable, arg='arg'):
		if not types.tuple_check(self.types, variable):
			types.type_error(arg, self)


	def __str__(self):
		return types.str_of(self)