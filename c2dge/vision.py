from .modules import avc
from . import const


s = avc.Int(_check='%d % 2 != 0')
size = [s, s]

@avc.TypeCheck
def vision(center: const.COORDS, size: size, _map: [list, ...], advance_by=1):
	vision = []
	base_map_x = int(center[0] - (size[0] / 2))
	base_map_y = int(center[1] - (size[1] / 2))

	if base_map_x < 0: base_map_x = 0
	elif base_map_x > len(_map[0]): base_map_x = len(_map[0]) - size[0]
	if base_map_y < 0: base_map_y = 0
	elif base_map_y > len(_map): base_map_y = len(_map) - size[1]

	map_x, map_y = base_map_x, base_map_y
	for y in range(size[1]):
		vision.append([])
		for x in range(size[0]):
			vision[y].append(_map[map_y][map_x])
			map_x += 1
		map_x = base_map_x
		map_y += 1
	return vision