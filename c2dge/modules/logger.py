from datetime import datetime
from colorama import Fore
from . import avc



class Logger:
	__logs__ = []
	__output__ = None
	__active__ = False
	__log_format__ = "%m %d: %e"


	@classmethod
	def _err(cls, msg: str, mode: str, col: str):
		mode = getattr(Fore, col.upper()) + mode + Fore.RESET
		date = str(datetime.now())
		
		text = cls.__log_format__\
			.replace('%m', mode)\
			.replace('%d', date)\
			.replace('%e', msg)

		if cls.__output__ != None:
			with open(cls.__output__, 'a', encoding='utf-8') as log_file:
				log_file.write(text + '\n')

		cls.__logs__.append(text)
		return text


	@classmethod
	@avc.TypeCheck
	def set_output(cls, file: avc.File()):
		cls.__output__ = file


	@classmethod
	def change_status(cls):
		cls.__active__ = not cls.__active__


	@classmethod
	def warning(cls, msg: str):
		if cls.__active__:
			return cls._err(msg, 'WARNING', 'lightred_ex')


	@classmethod
	def debug(cls, msg: str):
		if cls.__active__:
			return cls._err(msg, 'DEBUG', 'lightblack_ex')


	@classmethod
	def info(cls, msg: str):
		if cls.__active__:
			return cls._err(msg, 'INFO', 'cyan')


	@classmethod
	def error(cls, msg: str):
		if cls.__active__:
			return cls._err(msg, 'ERROR', 'yellow')


	@classmethod
	def critical(cls, msg: str):
		if cls.__active__:
			return cls._err(msg, 'CRITICAL', 'red')