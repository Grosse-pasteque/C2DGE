from .modules import avc, convertor, image_mod, logger
from . import objects, mapr, event, const

import os
import cv2
import time
import numpy
import colorama



class Window:
	@avc.TypeCheck
	def __init__(
		self,
		player:		objects.Player=None,
		_map:		mapr.Map=None,
		actions:	const.ACTIONS={},
		pixel_char: str='██', # '▒▒', '  '
		logs:		avc.Union(bool, avc.File())=False,
		clear:		bool=True,
		clock_tick: avc.Union(int, float)=0.1
	):
		if clock_tick < 0.1:
			raise ValueError(
				"Caution: arg clock_tick can't be under 0.1s otherwise it will cause issues.")

		self.parameters = {
			'pixel_char':	pixel_char,
			'clock_tick':	clock_tick,
			'clear':		clear,
			'logs':			logs
		}

		self.player = player
		self.map = _map
		self.actions = actions

		self.image = None
		self.frame = ""
		self.update_image()

		if self.parameters['logs'] == True:
			self.parameters['logs'] = 'c2dge-logs.log'

		if isinstance(self.parameters['logs'], str):
			logger.Logger.set_output(self.parameters['logs'])
			logger.Logger.change_status()


	def call_actions(self):
		events_called = False
		event_passed = []
		for event, action in self.actions.items():
			if bool(event()):
				events_called = True
				args = []
				if 'pass_window' in event.parameters:
					args.append(self)

				if 'pass_condition_args' in event.parameters:
					args += list(event.condition.args)
				
				action(*args)

		if self.player != None:
			for event, action in self.player.actions.items():
				if bool(event()):
					events_called = True
					args = []
					if 'pass_window' in event.parameters:
						args.append(self)

					if 'pass_condition_args' in event.parameters:
						args += list(event.condition.args)

					action(*args)
		return events_called


	def clear(self):
		if os.name == 'nt':
			os.system('cls')
		else:
			os.system('clear')


	def update_image(self):
		if self.map == None:
			self.image = []
		else:
			self.image = self.map.get_image()
			
			if self.player != None:
				self.image = self.map.place(self.player, self.image)


	@avc.TypeCheck
	def show(self, force_frame: numpy.ndarray=None):
		if self.parameters['clear']:
			self.clear()

		if isinstance(force_frame, numpy.ndarray):
			self.image = force_frame

		self.frame = image_mod.convert(
			image_mod.resize(self.image),
			self.parameters['pixel_char']
		)
		print(self.frame)


	@avc.TypeCheck
	def run(self, auto_color_init: bool=True):
		if auto_color_init:
			colorama.init()

		dtime = 0
		self.show()
		while True:
			changed = [
				self.call_actions(),
				self.map.update(dtime, self.map.background.frame)
			]
			if any(changed):
				self.update_image()
				self.show()
			time.sleep(self.parameters['clock_tick'])
			dtime += self.parameters['clock_tick']