import curses
from entity import Entity
from time import sleep, time
from pathfinding import find_path
from utils import to_bin_list
from maps import map1

red_leds = 13

MAP_H, MAP_W = len(map1), len(map1[0])
DASH_H = 3
NUM_RED_LEDS = 18


player = Entity(25, 3, "@", 2)
entities: 'list[Entity]' = []


def window(stdscr: "curses._CursesWindow"):
    # get window size
    HEIGHT, WIDTH = stdscr.getmaxyx()
    print(f"map h: {MAP_H}, map w: {MAP_W}")

    # init curses
    curses.noecho()  # don't display inputs
    curses.cbreak()  # don't require enter keypress to read inputs
    stdscr.nodelay(True)  # non-blocking inputs
    stdscr.keypad(True)  # read arrow inputs
    curses.curs_set(0)  # hide cursor
    stdscr.clear()
    stdscr.refresh()

    # init colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)

    win1 = curses.newwin(MAP_H + 2, MAP_W + 2, 0, 0)
    dash_win = curses.newwin(DASH_H, MAP_W + 2, MAP_H + 2, 0)

    pad1 = curses.newpad(MAP_H, MAP_W + 1)
    dash_pad = curses.newpad(DASH_H, MAP_W + 1)

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
    last_entity_update_time = time()

    while True:
        pad1.clear()
        dash_pad.clear()

        # draw map
        for i, line in enumerate(map1):
            pad1.addstr(i, 0, line)

        # time since last entity update
        current_time = time()
        elapsed_time = current_time - last_entity_update_time
        
        for entity in entities:
            # update entity every 0.5 seconds
            if elapsed_time >= 0.5:
                chase_entity(entity, player, map1)
                # save last update
                last_entity_update_time = current_time
            add_entity(pad1, entity)
            

        # draw dashboard
        draw_leds(dash_pad, lights, 18, 0, 5)
        draw_leds(dash_pad, lights, 8, 45, 4)

        lights += 1

        match stdscr.getch():
            case curses.KEY_DOWN:
                move_char(0, 1, player)
            case curses.KEY_UP:
                move_char(0, -1, player)
            case curses.KEY_LEFT:
                move_char(-1, 0, player)
            case curses.KEY_RIGHT:
                move_char(1, 0, player)
            case 27:  # ESC
                break
        
        # draw player
        add_entity(pad1, player)
        pad1.refresh(0, 0, 1, 1, MAP_H, MAP_W)
        dash_pad.refresh(0, 0, MAP_H + 3, 1, MAP_H + DASH_H, MAP_W)

        # wait for next frame
        sleep(1./10)

    # end curses
    curses.nocbreak()
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
            print (f"next_x = {next_x}, next_y = {next_y}")

            # calculate the direction to move
            dir_x = next_x - chaser.x
            dir_y = next_y - chaser.y

            # move chaser
            move_char(dir_x, dir_y, chaser)
        else:
            pass

def add_entity(pad: 'curses._CursesWindow', entity):
    pad.addch(entity.y, entity.x, entity.rep, curses.color_pair(entity.color))

def move_char(x, y, entity: 'Entity'):
    current_y = entity.y
    current_x = entity.x
    print(f"x: {current_x}, y: {current_y}, char: {entity.rep}")
    new_y = current_y + y
    new_x = current_x + x

    if (
        new_x >= MAP_W
        or new_x < 0
        or new_y >= MAP_H
        or new_y < 0
        or map1[new_y][new_x] == "#"
        or hitbox(new_x, new_y)
    ):
        return False
    else:
        entity.y = new_y
        entity.x = new_x
        return True


def draw_leds(pad, lights, total, offset, color):
    """
    Draws an LED dashboard
    
    lights -- int to convert to binary and represent visually
    total  -- total amount of LEDs to display
    offset -- how much padding to the left
    color  -- curses color pair to represent led
    """
    if 2 ** total - 1 < lights:
        return False
    for i, num in enumerate(to_bin_list(lights, total)):
        location = offset + i + 1
        if num == 0:
            pad.addch(0, location + i, ".", curses.color_pair(6))
        else:
            pad.addch(0, location + i, "@", curses.color_pair(color))
        pad.addch(0, location + i + 1, " ")

def hitbox(x, y):
    for entity in entities:
        if entity.x == x and entity.y == y:
            return True
    return False

def main():
    curses.wrapper(window)


main()
