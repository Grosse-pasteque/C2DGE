from . import event
from .modules import avc


ACTIONS = {(event.Event, avc.Function())}
COORDS = [int, int]
DEFAULT_VELOCITY = [5, 5]
PX_VAL = avc.Int(0, 255)
RGB = [PX_VAL, PX_VAL, PX_VAL]
RGBA = [PX_VAL, PX_VAL, PX_VAL, PX_VAL]
PIXEL = avc.Union(RGB, RGBA)


CONSOLE_COLORS = {
	"black":		"0",
	"blue":			"1",
	"green":		"2",
	"lightcyan":	"3",
	"red":			"4",
	"magenta":		"5",
	"yellow":		"6",
	"white":		"7",
	"gray":			"8",
	"lightblue":	"9",
	"lightgreen":	"A",
	"cyan":			"B",
	"lightred":		"C",
	"lightmagenta":	"D",
	"lightyellow":	"E",
	"lightwhite":	"F"
}


CONSOLE_SIZE = {
	'x': 211,
	'y': 51
}

IMAGE_SIZE_LIMIT = {
	'x': int(CONSOLE_SIZE['x'] / 2), # /2 because 1 cubic pixel = 2 chars
	'y': CONSOLE_SIZE['y']
}

from . import objects # import here to avoid circular import
OBJECT = avc.Union(objects.Player, objects.Entity, objects.Object)
OBJECTS = [OBJECT, ...]