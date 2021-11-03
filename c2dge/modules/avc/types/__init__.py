from .pattern import Pattern

from .new_types import (
	File, Class, Module, Function, Union
)

from .better_types import (
	Int, Str, Dict, Container
)


CUSTOM_TYPES = (
	File, Class, Module, Function, Union,
	Int, Str, Dict, Container,
	Pattern
)


def tuple_check(pattern, variable):
	check = []
	for typ in pattern:
		try:
			# dont need to check if arg is str for File
			# because it will raise error
			if not isinstance(typ, Pattern):
				typ = Pattern(typ)
			res = typ.check(variable)
			
			# res is True if CType is correct
			# if not raiseerror: res is False
			check.append(res) # check is good
			
			if res:
				# dont need to check others because one is correct
				break
		except:
			check.append(False) # Fails
	return True in check


def str_of(of):
	attrs = ', '.join([
		"{}={!r}".format(attr, getattr(of, attr))
		for attr in dir(of)
		if not attr.startswith('_') and \
			str(type(getattr(of, attr))) not in ["<class 'function'>", "<class 'method'>"]
	])
	return "<{}{}>".format(
		of.__class__.__name__,
		(f" ({attrs})" if attrs != '' else '')
	).replace("<class '", '').replace("'>", '')


def type_error(arg, self):
	raise TypeError(
		f'arg: {arg} need to be a {self}.')