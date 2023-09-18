import curses
from entity import Entity
from time import sleep

cur_map = [
    "                                                                                             ",
    "          3                          3                                                       ",
    "          3                          3           3                      1                    ",
    "          3                          3           3               3                           ",
    "          3333333333333333333333333333                          3                    1       ",
    "                                                        1       3                            ",
    "                                                                          1                  ",
    "                                                                                             ",
    "      1                            3                                                   1     ",
    "                                   3   1                                  1                  ",
    "              1             33333333                      1                                  ",
    "                                   3                                                         ",
    "                                   3                                  3                      ",
    "                              1                                       3 1                    ",
    "                                                                      3                      ",
    "                                                                                             ",
    "                                                                                             ",
]

MAP_H, MAP_W = len(cur_map), len(cur_map[0])

player = Entity(10, 10, "@", 2)
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

    win1 = curses.newwin(MAP_H + 2, MAP_W + 2, 0, 0)
    pad1 = curses.newpad(MAP_H, MAP_W + 1)

    # win2 = curses.newwin(HEIGHT//2, WIDTH//2, 0, WIDTH//2)
    win1.attron(curses.color_pair(1))
    win1.bkgd("'", curses.color_pair(1))
    win1.border()
    win1.refresh()

    entities.append(Entity(50,6, "#", 3))
    entities.append(Entity(60,9, "#", 3))

    while True:
        pad1.clear()

        # draw map
        for i, line in enumerate(cur_map):
            pad1.addstr(i, 0, line)

        # draw entities
        for entity in entities:
            chase_entity(entity, player)
            add_entity(pad1, entity)


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

        # wait for next frame
        sleep(1./10)

    # end curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def chase_entity(chaser, chased):
    dir_x = chaser.x - chased.x
    dir_y = chaser.y - chased.y
    
    if dir_x < 0:
        move_char(1, 0, chaser)
    elif dir_x > 0:
        move_char(-1, 0, chaser)

    if dir_y < 0:
        move_char(0, 1, chaser)
    elif dir_y > 0:
        move_char(0, -1, chaser)

def add_entity(pad: 'curses._CursesWindow', entity):
    pad.addch(entity.y, entity.x, entity.rep, curses.color_pair(entity.color))

def move_char(x, y, entity):
    current_y = entity.y
    current_x = entity.x
    print(f"x: {current_x}, y: {current_y}")
    new_y = current_y + y
    new_x = current_x + x

    if (
        new_x >= MAP_W
        or new_x < 0
        or new_y >= MAP_H
        or new_y < 0
        or cur_map[new_y][new_x] == "3"
        or hitbox(new_x, new_y)
    ):
        return False
    else:
        entity.y = new_y
        entity.x = new_x
        return True

def hitbox(x, y):
    for entity in entities:
        if entity.x == x and entity.y == y:
            return True
    return False

def main():
    curses.wrapper(window)


main()
