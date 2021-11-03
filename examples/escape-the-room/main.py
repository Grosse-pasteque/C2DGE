import sys
sys.path.insert(0, '../..')

from c2dge import (
	Event,
	Window, Map, BackGround,
	Player, Object,
	PixelCollision, Collision
)

import random
import keyboard

from functools import partial



class Game:
	def __init__(self):
		self.key_event = lambda key, args: Event(
			partial(keyboard.is_pressed, (key)),
			parameters=(['pass_condition_args'] if args else [])
		)

		self.ACTIONS = {
			self.key_event('left', True):	self.move_player,
			self.key_event('right', True):	self.move_player
		}
		self.COLLISIONS = [
			PixelCollision([140, 70, 20]),
			Collision('button', responde=self.turn_button),
			Collision('door', responde=self.open_door, collide=False)
		]

		self.player = Player(
			image=f'assets/player/bodies/{random.randint(0, 7)}.png',
			coords=[50, 0],
			attributes={
				'velocity':		[5, 0],
				'collisions':	self.COLLISIONS
			},
			actions=self.ACTIONS
		)

		self.objects = [
			Object(image='assets/button/off.png', coords=[14, 5], attributes={'tags': ['button', 'on']}),
			Object(image='assets/button/off.png', coords=[90, 5], attributes={'tags': ['button', 'on']}),
			Object(image='assets/door/closed.png', coords=[49, 0], attributes={'tags': ['door', 'closed']})
		]

		self.background = BackGround("assets/background.png")
		self.map = Map(
			background=self.background,
			view='face',
			objects=self.objects
		)

		self.window = Window(
			player=self.player,
			clear=False,
			_map=self.map,
			actions={
				self.key_event('esc', False): lambda: exit()
			}
		)


	def move_player(self, direction: str):
		conv = {
			'left':		[-1, 'assets/player/left.png'],
			'right':	[1, 'assets/player/right.png']
		}
		x, image = conv[direction]
		self.player.move(
			x * self.player['velocity'][0], 0,
			self.background.frame
		)
		self.player.set_image(image)


	def turn_button(self, objects):
		butt = objects[0]
		if 'off' == butt['tags'][1]:
			butt.set_image('assets/button/on.png')
		else:
			butt.set_image('assets/button/off.png')
		butt['tags'][1] = 'on'


	def open_door(self, x):
		if self.objects[0]['tags'][1] == 'on' and self.objects[1]['tags'][1] == 'on':
			if self.objects[2]['tags'][1] == 'closed':
				self.objects[2]['tags'][1] = 'open'
				self.objects[2].set_image('assets/door/open.png')

			if self.player.coords == [50, 0]:
				exit()


	def run(self):
		self.window.run()



game = Game()
game.run()