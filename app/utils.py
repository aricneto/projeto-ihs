def to_bin_list(num, size):
    return [int(i) for i in f'{num:0{size}b}']

DOOR_TILE = "░"
WALL_TILE = "█"
NONE_TILE = " "
GRASS_TILE = "."
COIN_TILE = "o"
BLOCKING_TILES = [DOOR_TILE, WALL_TILE]
WALKABLE_TILES = [NONE_TILE, GRASS_TILE, COIN_TILE]

def toggle_door(y, x, _map):
    if _map[y][x] in WALKABLE_TILES:
        return DOOR_TILE
    else:
        return NONE_TILE
    
def open_door(y, x, _map):
    _map[y][x] = NONE_TILE

def close_door(y, x, _map):
    _map[y][x] = DOOR_TILE