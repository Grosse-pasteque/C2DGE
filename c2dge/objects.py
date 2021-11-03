from .modules import avc
from . import const, errors

import cv2
import numpy


@avc.TypeCheck
def get_hitbox(image, coords: list):
	sy, sx, _ = image.shape
	return [
		coords,
		[coords[0] + sx - 1, coords[1] + sy - 1]
	]


def get_objects():
	return [
		*Object.__all__,
		*Entity.__all__,
		*Player.__all__
	]


class Base:
	def __init__(
		self,
		image: 		avc.File(),
		coords:		const.COORDS,
		attributes: dict
	):		
		self.attributes = attributes
		if 'tags' not in self.attributes:
			self.attributes['tags'] = []
		if 'velocity' not in self.attributes:
			self.attributes['velocity'] = const.DEFAULT_VELOCITY
		
		self.image = None
		self.set_image(image)

		self.coords = coords
		self.last_move = None
		self.last_coords = None


	@avc.TypeCheck
	def set_image(self, image: avc.File()):
		self.image = cv2.cvtColor(cv2.imread(image, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)

	
	@avc.TypeCheck
	def hitbox(self, edit: const.COORDS=[0, 0]):
		return get_hitbox(self.image, [self.coords[0] + edit[0], self.coords[1] + edit[1]])


	@avc.TypeCheck
	def has_collisions(self, x: int, y: int, image: numpy.ndarray=None):
		if 'collisions' in self.attributes:
			# only 1 tag collision
			collisions = self.attributes['collisions']
			if not isinstance(collisions, list):
				collisions = [collisions]

			check = []
			for col in collisions:
				if col.__class__.__name__ == 'PixelCollision' and isinstance(image, numpy.ndarray):
					check.append(col.has_collisions(self, [x, y], image))
				elif col.__class__.__name__ == 'Collision':
					check.append(bool(col.has_collisions(self, [x, y])))
				else:
					raise errors.InvalidCollision(
						f"collision: {col} is not a valid format !")
			return any(check)
		return False


	@avc.TypeCheck
	def move(self, x: int=0, y: int=0, /, image: numpy.ndarray=None):
		# default args will not change anything
		args = ((x, y, image) if isinstance(image, numpy.ndarray) else (x, y))
		if not self.has_collisions(*args):
			self.last_move = [x, y]
			self.last_coords = self.coords.copy()

			self.coords[0] += x
			self.coords[1] += y


	@avc.TypeCheck
	def is_on(self, image: numpy.ndarray, x: int=0, y: int=0):
		box = self.hitbox(edit=[x, y])
		pxs = []
		for y in range(box[0][1], box[1][1] + 1):
			for x in range(box[0][0], box[1][0] + 1):
				pxs.append(image[y][x].tolist())
		return pxs


	def update(self, var, value):
		if var in dir(self):
			setattr(self, var, value)


	@avc.TypeCheck
	def __setitem__(self, key: str, value):
		self.attributes[key] = value


	@avc.TypeCheck
	def __getitem__(self, key: str):
		return self.attributes[key]



class Entity(Base):
	__all__ = []


	@avc.TypeCheck
	def __init__(
		self,
		image: 		avc.File(),
		coords:		const.COORDS=[0, 0],
		attributes: dict={}
	):
		Entity.__all__.append(self)
		Base.__init__(self, image, coords, attributes)



class Player(Base):
	__all__ = []


	@avc.TypeCheck
	def __init__(
		self,
		image: 		avc.File(),
		coords:		const.COORDS=[0, 0],
		actions:	const.ACTIONS={},
		attributes: dict={}
	):
		Player.__all__.append(self)
		Base.__init__(self, image, coords, attributes)
		self.actions = actions



class Object(Base):
	__all__ = []


	@avc.TypeCheck
	def __init__(
		self,
		image: 		avc.File(),
		coords:		const.COORDS=[0, 0],
		fixed:		bool=False,
		attributes: dict={}
	):
		Object.__all__.append(self)
		Base.__init__(self, image, coords, attributes)
		self.fixed = fixed



class Animation:
	"""
	Comming soon
	"""
	pass