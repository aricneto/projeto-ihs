import curses
import _curses

cur_map = [
    "                                                                                             ",
    "          3                          3                                                       ",
    "          3                          3                                 1                     ",
    "          3                          3                                                       ",
    "          3333333333333333333333333333                                               1       ",
    "                                                        1                                    ",
    "                                                                          1                  ",
    "                                                                                             ",
    "      1                                                                                1     ",
    "                                       1                                  1                  ",
    "              1                                           1                                  ",
    "                                                                                             ",
    "                                                                                             ",
    "                              1                                         1                    ",
    "                                                                                             ",
    "                                                                                             ",
    "                                                                                             ",
]

char_dict = {
    "rep": "@",
    "y": 10,
    "x": 10
}

def window(stdscr: 'curses._CursesWindow'):
    # get window size
    HEIGHT, WIDTH = stdscr.getmaxyx()

    # init curses
    curses.noecho() # don't display inputs
    curses.cbreak() # don't require enter keypress to read inputs
    stdscr.keypad(True) # read arrow inputs
    curses.curs_set(0) # hide cursor
    stdscr.clear()
    stdscr.refresh()

    # init colors
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)

    win1 = curses.newwin(HEIGHT, WIDTH, 0, 0)
    pad1 = curses.newpad(17, 94)

    #win2 = curses.newwin(HEIGHT//2, WIDTH//2, 0, WIDTH//2)
    win1.attron(curses.color_pair(1))
    win1.bkgd('\'', curses.color_pair(1))
    win1.border()
    win1.refresh()

    while True:
        pad1.clear()
        for i, line in enumerate(cur_map):
             pad1.addstr(i, 0, line)

        match stdscr.getch():
            case curses.KEY_DOWN:
                move_char(0, 1)
            case curses.KEY_UP:
                move_char(0, -1)
            case curses.KEY_LEFT:
                move_char(-1, 0)
            case curses.KEY_RIGHT:
                move_char(1, 0)
            case 27: # ESC
                break
        
        pad1.addch(char_dict["y"], char_dict["x"], char_dict["rep"], curses.color_pair(2))
        pad1.refresh(0,0, 10,10, HEIGHT-1, WIDTH-1)

    # end curses
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()

def move_char(x, y):
    current_y = char_dict["y"]
    current_x = char_dict["x"]
    print (f"x: {current_x}, y: {current_y}")
    new_y = current_y + y
    new_x = current_x + x

    if (cur_map[new_y][new_x] == '3'):
        return False
    else:
        char_dict["y"] = new_y
        char_dict["x"] = new_x
        return True

def main():
    curses.wrapper(window)

main()