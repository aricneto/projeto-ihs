def to_bin_list(num, size):
    return [int(i) for i in f'{num:0{size}b}']

DOOR_TILE = "░"
WALL_TILE = "█"
BLOCKING_TILES = [DOOR_TILE, WALL_TILE]