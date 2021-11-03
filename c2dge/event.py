from functools import partial
from .modules import avc



class Event:
	__all__ = []


	@avc.TypeCheck
	def __init__(
		self,
		condition:		partial,
		parameters:		[str, ...]=[]
	):
		Event.__all__.append(self)
		self.condition = condition
		self.parameters = parameters


	def __call__(self):
		return self.condition()