from .main import TypeCheck
from .types import *
from .errors import IncorrectPatternError, IncorrectFileExtensionError

r"""
need to be changed to be able to use this module

	
In file ~~~~~~~~~~~~~~~~~~~~~~~~~~~
	from inspect import getfile
	import typing
	print(getfile(typing))
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


typing:1306 windows
typing:1369 linux
"def get_type_hints(obj, globalns=None, localns=None, include_extras=False, change_opt=True):"

typing:1387 windows
typing:1450 linux
"        if name in defaults and defaults[name] is None and change_opt:"


this will just make a functionnality optionnal
all the other programs will work the same way dont worry
"""



__all__ = (
	'TypeCheck',
	'File', 'Class', 'Module', 'Function', 'Union',
	'Int', 'Str', 'Dict', 'Container',
	'Pattern',
	'tuple_check', 'str_of', 'type_error',
	'IncorrectPatternError', 'IncorrectFileExtensionError',
)

__version__ = '0.6.0'
__author__ = (
	'Grosse pastèque#6705',
	'https://github.com/Grosse-pasteque',
	'Big watermelon'
)