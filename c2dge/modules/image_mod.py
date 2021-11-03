from . import avc
from .. import const
from .convertor import Color

import cv2
import numpy
import colorama


@avc.TypeCheck
def merge(back: numpy.ndarray, front: numpy.ndarray, x: int, y: int):
	if back.shape[2] == 3:
		back = cv2.cvtColor(back, cv2.COLOR_BGR2BGRA)

	if front.shape[2] == 3:
		front = cv2.cvtColor(front, cv2.COLOR_BGR2BGRA)

	bh, bw = back.shape[:2]
	fh, fw = front.shape[:2]
	x1, x2 = max(x, 0), min(x + fw, bw)
	y1, y2 = max(y, 0), min(y + fh, bh)
	front_cropped = front[y1 - y:y2 - y, x1 - x:x2 - x]
	back_cropped = back[y1:y2, x1:x2]

	alpha_front = front_cropped[:,:,3:4] / 255
	alpha_back = back_cropped[:,:,3:4] / 255
	
	result = back.copy()
	result[y1:y2, x1:x2, :3] = alpha_front * front_cropped[:,:,:3] + (1-alpha_front) * back_cropped[:,:,:3]
	result[y1:y2, x1:x2, 3:4] = (alpha_front + alpha_back) / (1 + alpha_front*alpha_back) * 255
	return result


@avc.TypeCheck
def resize(img: numpy.ndarray):
	height, width, depht = img.shape
	if width > const.IMAGE_SIZE_LIMIT['x']:
		img = cv2.resize(
			img,
			(
				const.IMAGE_SIZE_LIMIT['x'],
				int(round(height * const.IMAGE_SIZE_LIMIT['x'] / width, 0))
			)
		)
		return resize(img)

	if height > const.IMAGE_SIZE_LIMIT['y']:
		img = cv2.resize(
			img,
			(
				int(round(width * const.IMAGE_SIZE_LIMIT['y'] / height, 0)),
				const.IMAGE_SIZE_LIMIT['y']
			)
		)
	return img


@avc.TypeCheck
def zoom(image: numpy.ndarray):
	x, y, depth = image.shape
	if x > y:
		new_size = (const.IMAGE_SIZE_LIMIT['x'], y * const.IMAGE_SIZE_LIMIT['x'] / x)
	elif y < x:
		new_size = (x * const.IMAGE_SIZE_LIMIT['y'] / y, const.IMAGE_SIZE_LIMIT['x'])
	else:
		new_size = (const.IMAGE_SIZE_LIMIT['x'], const.IMAGE_SIZE_LIMIT['y'])
	return cv2.resize(image, new_size)


@avc.TypeCheck
def convert(frame: numpy.ndarray, pixel_char: str):
	# colored text frame
	ct_frame = ""
	for line in frame:
		for pixel in line:
			ct_frame += Color.to_color(Color.convert(pixel.tolist()[:3])) + pixel_char
		ct_frame += '\n'
	return ct_frame[:-1] + colorama.Fore.RESET