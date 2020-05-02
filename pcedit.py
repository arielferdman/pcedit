import curses
import curses.textpad
import wrapper as my

QUIT_KEY = 'q'
HORIZONTAL_LINE_CHAR = '\u2500'
TOP_RIGHT_CORNER_CHAR = '\u256E'
VERTIACL_LINE_CHAR = '\u2502'
BOTTOM_RIGHT_CORNER_CHAR = '\u2518'
BOTTOM_LEFT_CORNER_CHAR = '\u2514'
TOP_LEF_CORNER_CHAR = '\u250C'


class Editor:
    def __init__(self, stdscr):
        self.k = 0
        self.oy = 0
        self.ox = 0
        self.stdscr = stdscr
        self.sub = None
        self.help_box_dimensions = None

    def refresh_hook(self):
        self.draw_help_box(5, 120, 4, 10)
        self.print_to_help_box('q - quit')
        self.stdscr.original_refresh()

    def restore_cursor_position(self):
        self.move_cursor_absolute(self.oy, self.ox)

    def save_cursor_position(self):
        self.oy, self.ox = self.stdscr.getyx()

    def print_to_help_box(self, msg):
        if self.help_box_dimensions:
            self.move_cursor_absolute(self.help_box_dimensions.get(
                'y') + 1, self.help_box_dimensions.get('x') + 1)
            self.stdscr.addstr(msg)
            self.restore_cursor_position()

    def move_cursor_absolute(self, y, x):
        self.save_cursor_position()
        self.stdscr.move(y, x)

    def move_cursor_relative(self, y, x):
        self.save_cursor_position()
        self.stdscr.move(self.oy + y, self.ox + x)

    def repeat_horizontal_char(self, ch, no):
        for i in range(no):
            self.print_char(ch)

    def repeat_vertical_char(self, ch, no):
        oy, ox = self.stdscr.getyx()
        cy, cx = oy + 1, ox - 1
        for i in range(no):
            self.move_cursor_absolute(cy, cx)
            self.print_char(ch)
            cy += 1

    def draw_help_box(self, y, x, h, w):
        self.help_box_dimensions = {
            'y': y,
            'x': x,
            'h': h,
            'w': w,
        }

        self.move_cursor_absolute(y, x)
        self.repeat_horizontal_char(HORIZONTAL_LINE_CHAR, w)
        self.stdscr.addch(TOP_RIGHT_CORNER_CHAR)
        self.repeat_vertical_char(VERTIACL_LINE_CHAR, h)
        self.move_cursor_relative(1, -1)
        self.stdscr.addch(BOTTOM_RIGHT_CORNER_CHAR)
        self.move_cursor_absolute(y + h + 1, x)
        self.repeat_horizontal_char(HORIZONTAL_LINE_CHAR, w)
        self.move_cursor_relative(0, -w - 1)
        self.stdscr.addch(BOTTOM_LEFT_CORNER_CHAR)
        self.move_cursor_relative(-h - 1, 0)
        self.repeat_vertical_char(VERTIACL_LINE_CHAR, h)
        self.move_cursor_relative(-h, -1)
        self.stdscr.addch(TOP_LEF_CORNER_CHAR)
        self.move_cursor_absolute(0, 0)

    def read_char(self):
        return self.stdscr.getch()

    def initialize_cursor(self):
        curses.noecho()
        curses.curs_set(1)
        curses.cbreak()
        self.stdscr.keypad(True)

    def x_pressed(self):
        return self.k == ord(QUIT_KEY)

    def print_at_bottom(self, v):
        self.save_cursor_position()
        y, x = self.stdscr.getmaxyx()
        self.move_cursor_absolute(y - 1, 0)
        self.stdscr.addch(v)
        self.restore_cursor_position()

    def print_char(self, ch):
        self.stdscr.addch(ch)

    def main_loop(self):
        while not self.x_pressed():
            y, x = self.stdscr.getyx()
            self.draw_help_box(5, 120, 4, 10)
            self.print_to_help_box('q - quit')
            self.move_cursor_absolute(y, x)
            self.k = self.read_char()
            self.print_char(self.k)

    def start(self):
        self.initialize_cursor()
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
