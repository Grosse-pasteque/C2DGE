from . import avc



class Vector2:
	@avc.TypeCheck
	def __init__(self, x: int, y: int):
		self.x = x
		self.y = y


	@avc.TypeCheck
	def __iadd__(self, other: Vector2):
		self.x += other.x
		self.y += other.y


	@avc.TypeCheck
	def __isub__(self, other: Vector2):
		self.x -= other.x
		self.y -= other.y


	@avc.TypeCheck
	def __imul__(self, other: Vector2):
		self.x *= other.x
		self.y *= other.y


	@avc.TypeCheck
	def __idiv__(self, other: Vector2):
		self.x /= other.x
		self.y /= other.y


	@avc.TypeCheck
	def __ifloordiv__(self, other: Vector2):
		self.x //= other.x
		self.y //= other.y


	@avc.TypeCheck
	def __ipow__(self, other: Vector2):
		self.x **= other.x
		self.y **= other.y


	@avc.TypeCheck
	def __imod__(self, other: Vector2):
		self.x %= other.x
		self.y %= other.y


	@avc.TypeCheck
	def __ilshift__(self, other: Vector2):
		self.x <<= other.x
		self.y <<= other.y


	@avc.TypeCheck
	def __irshift__(self, other: Vector2):
		self.x >>= other.x
		self.y >>= other.y


	@avc.TypeCheck
	def __iand__(self, other: Vector2):
		self.x &= other.x
		self.y &= other.y


	@avc.TypeCheck
	def __ior__(self, other: Vector2):
		self.x |= other.x
		self.y |= other.y


	@avc.TypeCheck
	def __ixor__(self, other: Vector2):
		self.x ^= other.x
		self.y ^= other.y