from .. import types, errors


class Pattern:
	def __init__(self, pattern, raiseerror=True, containers=(list, tuple)):
		self.raiseerror = raiseerror
		self.pattern = pattern
		self.containers = containers


	def _ret(self, value, arg):
		if self.raiseerror:
			raise errors.IncorrectPatternError(
				f"arg: {arg!r} with value of {value!r} does not match Pattern: {self.pattern!r}")
		return False


	def is_infinite(self, val):
		if isinstance(val, (list, tuple)) and (len(val) == 2):
			if (val[1] == ...):
				if isinstance(val[0], (tuple, type)) or isinstance(val[0], types.CUSTOM_TYPES):
					return True
		return False


	def check(self, variable, arg=None):

		def _check(variable, pattern, arg, default_var):
			if isinstance(pattern, self.containers) and not self.is_infinite(pattern) :
				if not isinstance(variable, type(pattern)):
					return self._ret(default_var, arg) 
				
				for i, var in enumerate(variable):
					if len(variable) > len(pattern) or len(variable) < len(pattern):
						# prevent length error
						return self._ret(default_var, arg) 

					if isinstance(pattern[i], self.containers) and not self.is_infinite(pattern[i]):
						if len(pattern[i]) < len(var) or len(pattern[i]) > len(var):
							return self._ret(default_var, arg) 

					res = _check(
						variable[var] if isinstance(pattern, dict) else var,
						pattern[i],
						arg,
						default_var
					)

					if not res:
						return self._ret(default_var, arg) 

			elif self.is_infinite(pattern):
				if not isinstance(variable, type(pattern)):
					return self._ret(default_var, arg) 

				for var in variable:
					if isinstance(pattern[0], tuple):
						if not types.tuple_check(pattern[0], var):
							return self._ret(default_var, arg)
					elif isinstance(pattern[0], types.CUSTOM_TYPES):
						pattern[0].check(var, arg)
					elif not isinstance(var, pattern[0]):
						return self._ret(default_var, arg)

			elif isinstance(pattern, set):
				"""
				{
					(key-type, value-type),
					(min-length: int, max-length: int) or max-length: int
				}
				"""
				pattern = list(pattern)[::-1]
				# [::-1] for invertion because int is first in sort

				if isinstance(pattern[0], tuple):
					if not isinstance(variable, dict):
						return self._ret(default_var, arg) 

					if len(pattern) > 2:
						raise ValueError(
							"dict in pattern with set length/infinite can't have a length > 3.")

					if len(pattern) == 2: # has defined length
						err = "length of custom dict need to be a (int or None, int or None) or int"

						if not isinstance(pattern[1], (tuple, int)):
							raise ValueError(err)
						
						if isinstance(pattern[1], tuple):
							if len(pattern[1]) != 2:
								raise ValueError(err)

							condition = [
								isinstance(t, int)
								for t in pattern[1]
								if t != None
							]

							if False in condition:
								raise ValueError(err)

							if pattern[1][0] >= pattern[1][1]:
								raise ValueError(
									"dict set length, minimal length need to be < than max length")

							if pattern[1][0] != None: # min length is not infinite/undifinded
								if len(variable) < pattern[1][0]:
									return self._ret(default_var, arg) 

							if pattern[1][1] != None: # max length is not infinite/undifinded
								if len(variable) > pattern[1][1]:
									return self._ret(default_var, arg) 

						else: # int
							# can't have set length to be infinite because default is infinite 
							if len(variable) > pattern[1]:
								return self._ret(default_var, arg) 

					kv_check = "dict with set length need to be like {(key, val), length}"
					if not isinstance(pattern[0], tuple):
						raise ValueError(
							kv_check)

					if len(pattern[0]) != 2:
						raise ValueError(
							kv_check)

					for key, val in variable.items():
						if pattern[0][0] != None:
							res = _check(
								key,
								pattern[0][0],
								arg,
								default_var
							)
							
							if not res:
								self._ret(default_var, arg)

						if pattern[0][1] != None:
							res = _check(
								val,
								pattern[0][1],
								arg,
								default_var
							)
							
							if not res:
								self._ret(default_var, arg)
				
				else:
					if not types.tuple_check(pattern, variable):
						return self._ret(default_var, arg) 

			elif isinstance(pattern, dict):
				if not isinstance(variable, dict):
					return self._ret(default_var, arg) 

				if len(pattern) != len(variable):
					return self._ret(default_var, arg) 

				loop = zip(pattern.items(), variable.items()) # (key-type, val-type), (key, val)

				for p, v in loop:
					key_type, value_type = p
					key, value = v

					condition = [
						isinstance(key_type, tuple) and \
						True in [(type(t) in types.CUSTOM_TYPES) for t in key_type],
						isinstance(value_type, tuple) and \
						True in [(type(t) in types.CUSTOM_TYPES) for t in value_type]
					]

					if any(condition):
						raise AttributeError(
							"can't use custom types with multipule types in dict keys and values")

					if key_type != None:
						if isinstance(key_type, types.CUSTOM_TYPES):
							if isinstance(key_type, types.File) and not isinstance(key, str):
								return self._ret(default_var, arg) 
							key_type.check(key, arg)

						elif not isinstance(key, key_type):
							return self._ret(default_var, arg) 

					if value_type != None:
						if isinstance(value_type, types.CUSTOM_TYPES):
							if isinstance(key_type, types.File) and not isinstance(value, str):
								return self._ret(default_var, arg) 
							value_type.check(value, arg)

						elif not isinstance(value, value_type):
							return self._ret(default_var, arg) 

			elif isinstance(pattern, types.CUSTOM_TYPES):
				if not isinstance(variable, str) and isinstance(pattern, types.File):
					return self._ret(default_var, arg) 
				pattern.check(variable, arg)

			elif pattern == None:
				pass

			else:
				if not isinstance(variable, pattern):
					return self._ret(default_var, arg) 

			return True

		return _check(variable, self.pattern, arg, default_var=variable)


	def __str__(self):
		return types.str_of(self)