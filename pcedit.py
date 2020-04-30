import curses
import wrapper as my


def start(stdscr):
    k = 0
    while k != ord('q'):
        initialize_curser(stdscr)
        k = stdscr.getch()
        if k == 27:
            print_at_bottom(stdscr, ':')
        stdscr.addch(k)


def initialize_curser(stdscr):
    curses.noecho()
    curses.curs_set(1)
    curses.cbreak()
    stdscr.keypad(True)


def print_at_bottom(stdscr, v):
    oy, ox = stdscr.getyx()
    y, x = stdscr.getmaxyx()
    stdscr.move(y - 1, 0)
    stdscr.addch(v)
    stdscr.move(oy, ox)


def main(stdscr):
    try:
        start(stdscr)
    except Exception as ex:
        pass


if __name__ == '__main__':
    my.wrapper(main)
