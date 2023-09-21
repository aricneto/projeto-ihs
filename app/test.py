import curses
from comms import Comms
from entity import Entity
from time import sleep, time
from pathfinding import find_path
from utils import BLOCKING_TILES, COIN_TILE, DOOR_TILE, NONE_TILE, WALL_TILE, close_door, open_door, to_bin_list, toggle_door
from maps import map1

red_leds = 13

MAP_H, MAP_W = len(map1), len(map1[0])
DASH_H = 3
DASH_H = 4
SWITCH_H = 4
NUM_RED_LEDS = 18


player = Entity(25, 3, "@", 2)
entities: 'list[Entity]' = []
comms = Comms()

def window(stdscr: "curses._CursesWindow"):
    # get window size
    HEIGHT, WIDTH = stdscr.getmaxyx()

    # init curses
    curses.noecho()  # don't display inputs
    curses.cbreak()  # don't require enter keypress to read inputs
    stdscr.nodelay(True)  # non-blocking inputs
    stdscr.keypad(True)  # read arrow inputs
    curses.curs_set(0)  # hide cursor
    stdscr.clear()
    stdscr.refresh()

    # init colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   # bg
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # char
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)  # minotaur
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)  # led g
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)    # led v
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)  # off
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(8, curses.COLOR_RED, curses.COLOR_RED) # doors
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_YELLOW) # you won

    win1 = curses.newwin(MAP_H + 2, MAP_W + 2, 0, 0)
    dash_win = curses.newwin(DASH_H, MAP_W + 2, MAP_H + 2, 0)

    pad1 = curses.newpad(MAP_H, MAP_W + 1)
    dash_pad = curses.newpad(DASH_H, MAP_W + 1)
    switch_pad = curses.newpad(DASH_H, MAP_W + 1)

    win1.attron(curses.color_pair(1))
    win1.bkgd("'", curses.color_pair(1))
    win1.border()
    win1.refresh()

    dash_win.attron(curses.color_pair(1))
    dash_win.bkgd("'", curses.color_pair(1))
    dash_win.border()
    dash_win.refresh()

    entities.append(Entity(4, 6, "&", 3))
    # entities.append(Entity(60,9, "#", 3))

    lights = 0
    coins = 0
    max_coins = 18
    last_entity_update_time = time()
    start_map = [list(row) for row in map1]

    game_over = False
    you_won = False

    while True:
        pad1.clear()
        dash_pad.clear()
        switch_pad.clear()
        win1.addstr(0, 3, f"|coins:_{coins}|")
        win1.refresh()


        # draw map
        for i, line in enumerate(start_map):
            for j, tile in enumerate(line):
                pair = 1
                if tile == DOOR_TILE:
                    pair = 8
                if tile == COIN_TILE:
                    pair = 9
                pad1.addch(i, j, tile, curses.color_pair(pair))

        current_time = time()

        # time since last entity update
        elapsed_time = current_time - last_entity_update_time
        
        for entity in entities:

            # update entity every x seconds
            if elapsed_time >= 0.3:
                chase_entity(entity, player, start_map)
                # save last update
                last_entity_update_time = current_time
            add_entity(pad1, entity)

            # end game if entity touches player
            if entity.y == player.y and entity.x == player.x:
                message = "Game Over!"
                pad1.clear()
                pad1.addstr(MAP_H//2, MAP_W//2 - len(message) // 2, message)
                pad1.refresh(0, 0, 1, 1, MAP_H, MAP_W)
                game_over = True
                break
        
        if game_over:
            break

        # read switches and buttons
        switches = to_bin_list(comms.le_switch(), 18)
        buttons = to_bin_list(comms.le_botao(), 4)

        # draw dashboard
        draw_leds(dash_pad, to_bin_list(lights, 18), 18, 0, 5)
        draw_leds(dash_pad, to_bin_list(lights, 8), 8, 45, 4)

        draw_leds(switch_pad, buttons, 4, 49, 7, "_", "|", negate=True)
        draw_leds(switch_pad, switches, 18, 0, 7, "_", "|")

        #lights += 1

        # 4 push buttons act as directional keys (left, up, down, right)
        match comms.le_botao():
            case 0b1101:
                move_char(0, 1, player, start_map)
            case 0b1011:
                move_char(0, -1, player, start_map)
            case 0b0111:
                move_char(-1, 0, player, start_map)
            case 0b1110:
                move_char(1, 0, player, start_map)
            case 0b1010:  # ESC
                break
            
        # switches act as door toggles
        if (switches[17] == 1):
            close_door(4, 10, start_map)
        else:
            open_door(4, 10, start_map)

        if (switches[16] == 1):
            close_door(4, 35, start_map)
        else:
            open_door(4, 35, start_map)

        if (switches[15] == 1):
            close_door(6, 14, start_map)
        else:
            open_door(6, 14, start_map)

        if (switches[14] == 1):
            close_door(7, 3, start_map)
            close_door(7, 2, start_map)
            open_door(6, 28, start_map)
        else:
            open_door(7, 3, start_map)
            open_door(7, 2, start_map)
            close_door(6, 28, start_map)

        if (switches[13] == 1):
            close_door(5, 44, start_map)
            close_door(5, 46, start_map)
        else:
            open_door(5, 44, start_map)
            open_door(5, 46, start_map)

        if (switches[12] == 1):
            open_door(9, 31, start_map)
            close_door(10, 30, start_map)
        else:
            close_door(9, 31, start_map)
            open_door(10, 30, start_map)

        # collect coin
        if start_map[player.y][player.x] == COIN_TILE:
            coins += 1
            start_map[player.y][player.x] = NONE_TILE

        # end game when all coins are collected
        if coins == max_coins:
            message = " You won! "
            pad1.clear()
            pad1.addstr(MAP_H//2, MAP_W//2 - len(message) // 2, message, curses.color_pair(10))
            pad1.refresh(0, 0, 1, 1, MAP_H, MAP_W)
            you_won = True
            break
            

        # draw player
        add_entity(pad1, player)
        pad1.refresh(0, 0, 1, 1, MAP_H, MAP_W)
        dash_pad.refresh(0, 0, MAP_H + 3, 1, MAP_H + DASH_H - 1, MAP_W)
        switch_pad.refresh(0, 0, MAP_H + 4, 1, MAP_H + DASH_H, MAP_W)

        # wait for next frame
        # sleep(.1)
    
    while True:
        match stdscr.getch():
            case 27: # ESC 
                break

    # end curses
    comms.close()
    curses.nocbreak()
    stdscr.nodelay(False)
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def chase_entity(chaser, chased, map_data):
    # use A* pathfinding to find a path from chaser's current position to the target's position
    path = find_path(chaser.x, chaser.y, chased.x, chased.y, map_data)

    if path:
        if len(path) > 1:
            # move chaser towards the next point in the path
            next_x, next_y = path[1]

            # calculate the direction to move
            dir_x = next_x - chaser.x
            dir_y = next_y - chaser.y

            # move chaser
            move_char(dir_x, dir_y, chaser, map_data)
        else:
            pass

def add_entity(pad: 'curses._CursesWindow', entity: 'Entity'):
    pad.addch(entity.y, entity.x, entity.rep, curses.color_pair(entity.color) | curses.A_BOLD)

def move_char(x, y, entity: 'Entity', map_data):
    current_y = entity.y
    current_x = entity.x
    new_y = current_y + y
    new_x = current_x + x

    if (
        new_x >= MAP_W
        or new_x < 0
        or new_y >= MAP_H
        or new_y < 0
        or map_data[new_y][new_x] in BLOCKING_TILES
        or hitbox(new_x, new_y)
    ):
        return False
    else:
        entity.y = new_y
        entity.x = new_x
        return True


def draw_leds(pad, lights, total, offset, color, char_off=".", char_on="@", negate=False):
    """
    Draws an LED dashboard
    
    lights -- int to convert to binary and represent visually
    total  -- total amount of LEDs to display
    offset -- how much padding to the left
    color  -- curses color pair to represent led
    """
    # if total - 1 < len(lights):
    #     return False
    for i, num in enumerate(lights):
        if negate:
            num = not num
        location = offset + i + 1
        if num == 0:
            pad.addch(0, location + i, char_off, curses.color_pair(6))
        else:
            pad.addch(0, location + i, char_on, curses.color_pair(color))
        pad.addch(0, location + i + 1, " ")

def hitbox(x, y):
    for entity in entities:
        if entity.x == x and entity.y == y:
            return True
    return False

def main():
    curses.wrapper(window)


main()
