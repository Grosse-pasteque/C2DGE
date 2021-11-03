from .modules import avc, image_mod, convertor
from . import const, phisycs, objects, errors

import os
import cv2
import numpy
import random
from colorama import Fore



class BackGround:
	@avc.TypeCheck
	def __init__(
		self,
		config:	avc.Union(dict, list, str, numpy.ndarray),
		size:	const.COORDS=list(const.IMAGE_SIZE_LIMIT.values())
	):
		"""
		config:
			- [color: str]
			- {int: color}
			- color

		"""
		self.org_config = config
		self.config = config

		if isinstance(self.config, dict):
			temp = self.config.copy()
			self.config = []

			for n, color in temp.items():
				condition = [
					isinstance(n, int),
					color in convertor.Color.VALID_COLORS
				]

				if False in condition:
					raise TypeError(
						'dict config need to be like {int: Fore.color}')

				self.config += [color for loop in range(n)]

		if isinstance(self.config, str):
			if os.path.exists(self.config):
				self.frame = cv2.cvtColor(cv2.imread(self.config, cv2.IMREAD_UNCHANGED), cv2.COLOR_BGRA2RGBA)
				return

			if self.config not in const.CONSOLE_COLORS:
				raise ValueError(
					'arg: config is not a valid color !')

			if 'light' in self.config:
				self.config += '_ex'

			pixel = convertor.Color.to_pixel(self.config)
			frame = [
				[
					pixel + [255]
					for x in range(size[0])
				]
				for y in range(size[1])
			]

		if isinstance(config, numpy.ndarray):
			self.frame = config
			return
		
		else:
			frame = [
				[
					convertor.Color.to_pixel(
						random.choice(self.config)
					) + [255]
					for x in range(size[0])
				]
				for y in range(size[1])
			]

		self.frame = numpy.array(frame, dtype=numpy.uint8)



class Map:
	__all__ = []


	@avc.TypeCheck
	def __init__(
		self,
		background: BackGround,
		view: 		str='top',
		objects:	const.OBJECTS=[],
		gravity:	phisycs.Gravity=None
	):
		if view not in ['face', 'top']:
			raise ValueError(
				'arg: view can be either face or top !')

		if view == 'top' and gravity != None:
			raise AttributeError(
				"top view can't have gravity !")

		Map.__all__.append(self)
		self.view = view
		self.background = background
		self.gravity = gravity
		self.objects = objects


	# function to recode (for gravity)
	@avc.TypeCheck
	def update(self, dtime: avc.Union(int, float), image: numpy.ndarray=None):
		if self.view == 'face':
			if self.gravity != None:
				for obj in self.objects:
					args = [0, 0]
					if isinstance(image, numpy.ndarray):
						args.append(image)

					if not obj.has_collisions(*args):
						new_coords = self.gravity.step(obj, dtime)
						last_coords = obj.coords.copy()
						obj.coords = new_coords.copy()

						if obj.has_collisions(*args):
							obj.coords = last_coords.copy()
				return True
		return False


	@avc.TypeCheck
	def place(self, obj: const.OBJECT, on: numpy.ndarray):
		coords = obj.coords.copy()
		if self.view == 'face':
			coords = [coords[0], const.CONSOLE_SIZE['y'] - coords[1] - obj.image.shape[0]]
		return image_mod.merge(on, image_mod.resize(obj.image), *coords)

	
	def get_image(self):
		frame = self.background.frame.copy()
		for obj in self.objects:
			frame = self.place(obj, frame)
		return frame