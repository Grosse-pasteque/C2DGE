from functools import partial
import inspect
import typing

from . import types


def has_ctypes(_types):
	return True in [(t in types.CUSTOM_TYPES) for t in list(_types)]


def _raise_error(arg, typ, message):
	raise TypeError(
		message\
		.replace('%a', arg)\
		.replace('%t', str(typ))
	)


def _reformat_args(args, base):
	real_args = [p.split(':')[0] for p in str(base)[1:-1].replace(' ', '').split(',')]

	for i, _ in enumerate(zip(real_args, list(args.keys()))):
		part, key = _
		name = part.split(':')[0].split('=')[0].replace(' ', '')
		
		if key == name.replace('*', ''):
			values = args[key]
			args.pop(key)
			args[name] = values

	return args


def _reformat_types(anno):
	_types = anno.copy()
	for key, typ in _types.items():
		if isinstance(typ, tuple):
			temp = list(typ)
			for p, arg in enumerate(temp):
				if isinstance(arg, types.CUSTOM_TYPES):
					temp[p] = type(arg)

			_types[key] = tuple(temp)

		elif isinstance(typ, types.CUSTOM_TYPES):
			_types[key] = type(typ)

	return _types



class TypeCheck:
	def __init__(self, func):
		types.Function().check(func)

		self.func = func
		self.message = f"{func.__name__} arg: %a must be %t"
		self.__name__ = func.__name__

	
	def _check(self, *args, **kwargs):
		data = inspect.signature(self.func).bind(*args, **kwargs)

		arguments = _reformat_args(
			dict(data.arguments),
			data.signature
		)

		annotations = _reformat_args(
			typing.get_type_hints(self.func, change_opt=False),
			data.signature
		)

		req_types = _reformat_types(annotations)

		for name, value in arguments.items():
			if name in annotations:
				if name.startswith('*'):
					if isinstance(req_types[name], dict) or name.startswith('**'):
						value = tuple(value.values())

					for arg in value:
						types.Pattern(annotations[name]).check(arg, name)
				else:
					types.Pattern(annotations[name]).check(value, name)


	def __get__(self, instance, owner):
		return partial(self.__call__, instance)


	def __call__(self, *args, **kwargs):
		self._check(*args, **kwargs)
		return self.func(*args, **kwargs)