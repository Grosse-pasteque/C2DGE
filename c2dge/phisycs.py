from .modules import avc
from . import const, objects, errors

import math
import numpy



class Gravity:
	@avc.TypeCheck
	def __init__(self, g: float=9.81):
		"""
		to help you usualy g is:
		- 9.81 for earth
		- 6.67 for space


		m/s
		down_speed = 9.81 + 9.81 * dtime
		up_speed = obj['velocity'][1]
		horizontal_speed = obj['velocity'][0]

		total_speed = (up_speed - down_speed)


		~~~~~~~~~~{ FORMULA }~~~~~~~~~~~
			speed = distance / dtime
			distance = speed * dtime
		~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


		total_speed = math.sqrt( total_speed**2 + horizontal_speed**2 )



		"""
		self.g = g


	@avc.TypeCheck
	def step(self, obj: const.OBJECT, dtime: avc.Union(int, float)):
		# x = obj['velocity'][0] * dtime
		coords = obj.coords.copy()
		if coords[1] > 0:
			s = (obj['velocity'][1] if coords[1] == 0 else coords[1])
			y = round(s - (self.g * dtime)) * dtime
			y = (obj.image.shape[0] if y < 0 else y)
		else:
			y = coords[1]
		return [coords[0], y]



class Collision:
	def __init__(
		self,
		tag:		avc.Union(str, [str, ...]),
		responde:	avc.Function()=None,
		collide:	bool=True
	):
		if isinstance(tag, str):
			tag = [tag]
		self.tags = tag
		self.responde = responde
		self.collide = collide


	@avc.TypeCheck
	def has_collisions(self, obj: const.OBJECT, edit: const.COORDS):
		obj1 = obj.hitbox(edit=edit)
		all_objects = objects.get_objects()
		all_objects.remove(obj)

		collide_with = []
		for obj in all_objects:
			check = [
				tag in obj['tags']
				for tag in self.tags
			]
			if any(check):
				obj2 = obj.hitbox()
				check = {
					'x': [
						obj1[0][0] <= obj2[0][0] <= obj1[1][0],
						obj1[0][0] <= obj2[1][0] <= obj1[1][0]
					],
					'y': [
						obj1[0][1] <= obj2[0][1] <= obj1[1][1],
						obj1[0][1] <= obj2[1][1] <= obj1[1][1]
					]
				}

				check = [
					check['x'][0] and check['y'][0],
					check['x'][0] and check['y'][1],
					check['x'][1] and check['y'][0],
					check['x'][1] and check['y'][1]
				]

				if True in check:
					collide_with.append(obj)
		
		if len(collide_with) != 0 and self.responde != None:
			self.responde(collide_with)
		
		if self.collide:
			return collide_with
		return []



class PixelCollision:
	@avc.TypeCheck
	def __init__(
		self,
		pixel:		const.PIXEL,
		responde:	avc.Function()=None,
		pass_obj:	bool=False,
		collide:	bool=True
	):
		self.pixel = pixel
		self.responde = responde
		self.pass_obj = pass_obj
		self.collide = collide


	@avc.TypeCheck
	def has_collisions(self, obj: const.OBJECT, edit: const.COORDS, image: numpy.ndarray):
		pixels = obj.is_on(image, *edit)
		for px in pixels:
			if self.pixel[:3] == px:
				if self.responde:
					args = []
					if self.pass_obj:
						args.append(obj)
					self.responde(*args)
				if self.collide:
					return True
		return False
