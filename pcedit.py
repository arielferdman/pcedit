import curses
import wrapper as my

QUIT_KEY = 'q'


class Editor:
    def __init__(self, stdscr):
        self.k = 0
        self.stdscr = stdscr

    def read_char(self):
        return self.stdscr.getch()

    def experiment(self):
        self.stdscr.subwin()

    def initialize_cursor(self):
        curses.noecho()
        curses.curs_set(1)
        curses.cbreak()
        self.stdscr.keypad(True)

    def x_pressed(self):
        return self.k == ord(QUIT_KEY)

    def print_at_bottom(self, v):
        oy, ox = self.stdscr.getyx()
        y, x = self.stdscr.getmaxyx()
        self.stdscr.move(y - 1, 0)
        self.stdscr.addch(v)
        self.stdscr.move(oy, ox)
    
    def print_char(self):
        self.stdscr.addch(self.k)

    # if self.k == 27:
    #     self.print_at_bottom(':')
    def main_loop(self):
        while not self.x_pressed():
            self.initialize_cursor()
            self.k = self.read_char()

            self.print_char()

    def start(self):
        self.main_loop()


def main(stdscr):
    try:
        editor = Editor(stdscr)
        editor.start()
    except Exception as ex:
        print(ex)
        pass


if __name__ == '__main__':
    my.wrapper(main)
