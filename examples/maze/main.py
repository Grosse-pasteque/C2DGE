import sys
sys.path.insert(0, '../..')

from c2dge import (
	Event, Window, Map, BackGround, Player, Collision, PixelCollision,
	get_hitbox
)

import cv2
import time
import numpy
import keyboard
from pygame import mixer
from functools import partial



class Game:
	def __init__(self):
		self.key_event = lambda key, args: Event(
			partial(keyboard.is_pressed, (key)),
			parameters=(['pass_condition_args'] if args else [])
		)

		self.ACTIONS = {
			self.key_event('left', True):	self.move_player,
			self.key_event('right', True):	self.move_player,
			self.key_event('down', True):	self.move_player,
			self.key_event('up', True):		self.move_player,
			self.key_event('space', False):	self.break_wall
		}

		self.player = Player(
			image='assets/player.png',
			coords=[1, 1],
			attributes={
				'force':		3,
				'inventory':	[],
				'collisions':	PixelCollision([0, 0, 0])
			},
			actions=self.ACTIONS
		)

		self.maze_img = cv2.cvtColor(cv2.imread('assets/maze.png'), cv2.COLOR_BGR2RGB)
		self.map = Map(background=BackGround(self.maze_img))

		self.window = Window(
			player=self.player,
			_map=self.map,
			clear=False,
			actions={
				self.key_event('esc', False): lambda: exit()
			}
		)

		mixer.init()
		self.sounds = {
			'break-wall': mixer.Sound('assets/wall-break.mp3')
		}
		self.last_box = None


	def end_game(self):
		time.sleep(3)
		end_image = cv2.cvtColor(cv2.imread('assets/end-background.png'), cv2.COLOR_BGR2RGB)
		self.window.show(end_image)
		exit()


	def move_player(self, direction: str):
		conv = {
			'left':		(-2, 0),
			'right':	(2, 0),
			'up':		(0, -2),
			'down':		(0, 2)
		}

		x, y = self.player.coords
		px, py = conv[direction]
		box = get_hitbox(self.player.image, [x + px, y + py])
		if -1 in box[0] or 0 in box[1]:
			return
		self.last_box = box.copy()

		if [0, 200, 70] in self.player.is_on(self.maze_img, *conv[direction]):
			return self.end_game()
		self.player.move(*conv[direction], self.maze_img)


	def break_wall(self):
		if self.player['force'] > 0:
			if self.last_box != None:
				blocks = [
					self.last_box[0],
					self.last_box[1],
					[self.last_box[0][0], self.last_box[1][1]],
					[self.last_box[1][0], self.last_box[0][1]]
				]
				for block in blocks:
					x = int((self.player.coords[0] + block[0] + 1) / 2)
					y = self.player.coords[1] + block[1] - 1
					px = self.maze_img[y][x].tolist()
					if px[:3] == [0, 0, 0]:
						self.maze_img[y][x] = numpy.array([255, 255, 255], dtype=numpy.uint8)
						self.sounds['break-wall'].play()
				self.player.attributes['force'] -= 1


	def run(self):
		self.window.run()



game = Game()
game.run()