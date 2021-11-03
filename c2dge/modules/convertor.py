from . import avc
from .. import const

import webcolors
import colorama



class Color:
	CHANGER = {
		"aqua":		"cyan",
		"fuchsia":	"magenta",
		"gray":		"lightblack",
		"lime":		"lightgreen",
		"maroon":	"lightred",
		"navy":		"lightblue",
		"olive":	"lightyellow",
		"purple":	"lightmagenta",
		"silver":	"lightwhite",
		"teal":		"lightcyan"
	}

	VALID_COLORS = [
		col
		for col in dir(colorama.Fore)
		if not col.startswith('_')
	]


	@classmethod
	@avc.TypeCheck
	def convert(cls, pixel: const.PIXEL):
		min_colours = {}
		for key, name in webcolors.CSS2_HEX_TO_NAMES.items():
			r_c, g_c, b_c = webcolors.hex_to_rgb(key)
			rd = (r_c - pixel[0]) ** 2
			gd = (g_c - pixel[1]) ** 2
			bd = (b_c - pixel[2]) ** 2
			min_colours[(rd + gd + bd)] = name

		color = min_colours[min(min_colours.keys())]
		if color in cls.CHANGER:
			color = cls.CHANGER[color]
		
		if 'light' in color:
			color += '_ex'

		return color


	@classmethod
	@avc.TypeCheck
	def to_color(cls, color: str):
		if color.upper() in cls.VALID_COLORS:
			return eval(f"colorama.Fore.{color.upper()}")


	@classmethod
	@avc.TypeCheck
	def to_pixel(cls, color: str):
		col = color.replace('_ex', '')
		
		if color in cls.CHANGER.values():
			index = list(cls.CHANGER.values()).index(color)
			color = list(cls.CHANGER.keys())[index]

		index = list(webcolors.CSS2_HEX_TO_NAMES.values()).index(color)
		hex_color = list(webcolors.CSS2_HEX_TO_NAMES.keys())[index]
		return list(webcolors.hex_to_rgb(hex_color))