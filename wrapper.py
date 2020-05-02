from _curses import *


# class MyWindow(window):
#     def __init__(self, *args, **kwargs):
#         super(MyWindow, self).__init__(args, kwargs)
#         self.hook = kwargs.get('refresh_hook', None)
#
#     def refresh(self, pminrow=None, pmincol=None, sminrow=None, smincol=None, smaxrow=None, smaxcol=None):
#         if self.hook:
#             self.hook()
#
#         super(MyWindow, self).refresh(pminrow=None, pmincol=None, sminrow=None, smincol=None, smaxrow=None,
#                                       smaxcol=None)


def wrapper(*args, **kwds):
    """Wrapper function that initializes curses and calls another function,
    restoring normal keyboard/screen behavior on error.
    The callable object 'func' is then passed the main window 'stdscr'
    as its first argument, followed by any other arguments passed to
    wrapper().
    """
    # def refresh_hook():
    #     if
    #
    # original_refresh = refresh

    # refresh = refresh_hook

    if args:
        func, *args = args
    elif 'func' in kwds:
        func = kwds.pop('func')
        import warnings
        warnings.warn("Passing 'func' as keyword argument is deprecated",
                      DeprecationWarning, stacklevel=2)
    else:
        raise TypeError('wrapper expected at least 1 positional argument, '
                        'got %d' % len(args))

    try:
        # Initialize curses
        stdscr = initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        noecho()
        cbreak()

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)

        # Start color, too.  Harmless if the terminal doesn't have
        # color; user can test with has_color() later on.  The try/catch
        # works around a minor bit of over-conscientiousness in the curses
        # module -- the error return from C start_color() is ignorable.
        # try:
        #     start_color()
        # except:
        #     pass

        return func(stdscr, *args, **kwds)
    finally:
        # Set everything back to normal
        if 'stdscr' in locals():
            stdscr.keypad(0)
            echo()
            nocbreak()
            endwin()


wrapper.__text_signature__ = '(func, /, *args, **kwds)'
