import sys
sys.path.insert(0, '../..')


# Speedcode mon sauveur

from c2dge import (
	Event, Window, Map, BackGround, Object
)

import cv2
import time
import keyboard
from functools import partial



class Game:
	def __init__(self):
		self.ACTIONS = {
			Event(
				partial(keyboard.is_pressed, (str(i))),
				parameters=['pass_condition_args']
			): self.chose
			for i in range(1, 10) # for all cases
		}
		self.ACTIONS[Event(partial(keyboard.is_pressed, ('esc')))] = lambda: exit()

		self.background = BackGround("assets/background.png")
		self.map = Map(background=self.background)
		
		self.window = Window(
			_map=self.map,
			actions=self.ACTIONS
		)

		self.player_turn = 'cross'

		self.grid = [
			[None, None, None],
			[None, None, None],
			[None, None, None]
		]

		self.shapes_files = {
			'round': 'assets/round.png',
			'cross': 'assets/cross.png'
		}


	def win(self):
		# lines and column check
		for i in range(3):
			if any([
				self.grid[0][i] == self.grid[1][i] == self.grid[2][i] != None,	# line
				self.grid[i][0] == self.grid[i][1] == self.grid[i][2] != None	# column
			]):
				return True

		# diagonal check
		if any([
			self.grid[0][0] == self.grid[1][1] == self.grid[2][2] != None,
			self.grid[0][2] == self.grid[1][1] == self.grid[2][0] != None
		]):
			return True

		return False


	def end_game(self):
		image = cv2.cvtColor(cv2.imread("assets/end-background.png"), cv2.COLOR_BGR2RGB)
		image = self.map.place(
			Object(image=self.shapes_files[self.player_turn], coords=[18, 3]),
			image
		)
		image = cv2.putText(
			image,
			self.player_turn,
			(35, 18),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.75,
			(255, 255, 255),
			2,
			cv2.LINE_AA
		)

		self.window.show(self.map.get_image())

		time.sleep(3)
		self.window.show(image)

		time.sleep(3)
		keyboard.read_key()
		exit()


	def other(self):
		if self.player_turn == 'round':
			return 'cross'
		else:
			return 'round'


	def chose(self, case: str):
		convert = {
			'1': (0, 0), '2': (1, 0), '3': (2, 0),
			'4': (0, 1), '5': (1, 1), '6': (2, 1),
			'7': (0, 2), '8': (1, 2), '9': (2, 2)
		}

		x, y = convert[case]
		if self.grid[y][x] == None:
			self.grid[y][x] = self.player_turn

			# 3 pixel gap between cases
			# 15x15 pixel cases
			coords = [(x*15 + x*3), (y*15 + y*3)]

			case = Object(
				image=self.shapes_files[self.player_turn],
				coords=coords
			)

			self.map.objects.append(case)

			if self.win():
				self.end_game()

			self.player_turn = self.other()


	def run(self):
		self.window.run()



game = Game()
game.run()