from .. import types



class Int:
	def __init__(self, _min=None, _max=None, _check=None):
		# check : "0 < %d < 10"
		if all([_check != None, _min != None, _max != None]):
			raise AttributeError(
				"you can't use _min/_max args and check !")

		if _min != None and not isinstance(_min, int):
			raise TypeError(
				'arg: _min need to be int.')

		if _max != None and not isinstance(_max, int):
			raise TypeError(
				'arg: _max need to be int.')

		if _check != None and not isinstance(_check, str):
			raise TypeError(
				'arg: check need to be str.')

		self.min = _min
		self.max = _max
		self._check = _check


	def check(self, _int, arg='arg'):
		if not float(_int).is_integer():
			types.type_error(arg, self)

		if self.min != None:
			if self.min > _int:
				raise ValueError(
					f'arg: {arg} need to be <= {self.min}.')

		if self.max != None:
			if self.max < _int:
				raise ValueError(
					f'arg: {arg} need to be >= {self.max}.')

		if self._check != None:
			exp = self._check.replace('%d', str(_int))
			try:
				res = eval(exp)

			except:
				raise ValueError(
					f'expression: {repr(exp)} failled to execute !')

			if not res:
				raise ValueError(
					f"arg: {arg} doesn't respect check expression !")


	def __str__(self):
		return types.str_of(self)



class Str:
	def __init__(self, include=[], exclude=[], length=None, _check=None):
		# check: "'a' in %s"
		if not isinstance(include, list):
			raise TypeError(
				'arg: include need to be list.')
		
		if not isinstance(exclude, list):
			raise TypeError(
				'arg: exclude need to be list.')
		
		if length != None and not isinstance(length, int):
			raise TypeError(
				'arg: length need to be int.')

		if _check != None and not isinstance(_check, str):
			raise TypeError(
				'arg: check need to be str.')

		self.include = include
		self.exclude = exclude
		self.length = length
		self._check = _check


	def check(self, _str, arg='arg'):
		if not isinstance(_str, str):
			types.type_error(arg, self)

		for letter in self.include:
			if letter not in _str:
				raise ValueError(
					f'arg: {arg} need to include {repr(letter)}.')

		for letter in self.exclude:
			if letter in _str:
				raise ValueError(
					f'arg: {arg} need to exclude {repr(letter)}.')

		if len(_str) != self.length and self.length != None:
			raise ValueError(
				f'arg: {arg} need to have a length of {self.length}.')

		if self._check != None:
			exp = self._check.replace('%s', str(_str))
			try:
				res = eval(exp)

			except:
				raise ValueError(
					f'expression: {repr(exp)} failled to execute !')

			if not res:
				raise ValueError(
					f"arg: {arg} doesn't respect check expression !")


	def __str__(self):
		return types.str_of(self)



class Dict:
	def __init__(
		self,
		include_keys=[],
		exclude_keys=[],
		include_values=[],
		exclude_values=[],
		length=None
	):
		_check = [
			isinstance(include_keys, list),
			isinstance(exclude_keys, list),
			isinstance(include_values, list),
			isinstance(exclude_values, list)
		]

		if False in _check:
			raise TypeError(
				'arg: include_keys, exclude_keys, include_values, exclude_values need to be list.')
		
		if length != None and not isinstance(length, int):
			raise TypeError(
				'arg: length need to be int.')

		self.include_keys = include_keys
		self.exclude_keys = exclude_keys
		self.include_values = include_values
		self.exclude_values = exclude_values
		self.length = length


	def check(self, _dict, arg='arg'):
		if not isinstance(_dict, dict):
			types.type_error(arg, self)

		for key in self.include_keys:
			if key not in _dict:
				raise ValueError(
					f'arg: {arg} need to include key {repr(key)}.')

		for key in self.exclude_keys:
			if key in _dict:
				raise ValueError(
					f'arg: {arg} need to exclude key {repr(key)}.')
		
		for val in self.include_values:
			if val not in list(_dict.values()):
				raise ValueError(
					f'arg: {arg} need to include value {repr(val)}.')

		for val in self.exclude_values:
			if val in list(_dict.values()):
				raise ValueError(
					f'arg: {arg} need to exclude value {repr(val)}.')

		if len(_dict) != self.length and self.length != None:
			raise ValueError(
				f'arg: {arg} need to have a length of {self.length}.')


	def __str__(self):
		return types.str_of(self)



class Container:
	def __init__(self, _type, include=[], exclude=[], length=None):				
		allowed = (tuple, list, set)
		
		if not isinstance(_type, (type, tuple)):
			if _type not in allowed:
				raise TypeError(
					f'arg: _type need to be {allowed}.')

			raise TypeError(
				'arg: _type need to be a type or tuple of types.')

		if isinstance(_type, tuple):
			for typ in _type:
				if _type not in allowed:
					raise TypeError(
						f'arg: _type need to be {allowed}.')
				
				if not isinstance(typ, type):
					raise TypeError(
						'arg: _type need to be a type or tuple of types.')


		if not isinstance(include, list):
			raise TypeError(
				'arg: include need to be list.')
		
		if not isinstance(exclude, list):
			raise TypeError(
				'arg: exclude need to be list.')
		
		if length != None and not isinstance(length, int):
			raise TypeError(
				'arg: length need to be int.')

		self.type = _type
		self.include = include
		self.exclude = exclude
		self.length = length


	def check(self, container, arg='arg'):
		if not isinstance(container, self.type):
			types.type_error(arg, self)

		for var in self.include:
			if var not in container:
				raise ValueError(
					f'arg: {arg} need to include {repr(var)}.')

		for var in self.exclude:
			if var in container:
				raise ValueError(
					f'arg: {arg} need to exclude {repr(var)}.')

		if len(container) != self.length and self.length != None:
			raise ValueError(
				f'arg: {arg} need to have a length of {self.length}.')


	def __str__(self):
		return types.str_of(self)