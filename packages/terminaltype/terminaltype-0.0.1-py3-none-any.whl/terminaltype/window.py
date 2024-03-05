import curses

from terminaltype.text import clear_line
from terminaltype.colors import *


def init_screen(screen, test):
    """
    Initialize the top bar, print the test string

    Args:
        screen: curses screen
        test: name of the file
    """
    curses.noecho()
    curses.start_color()
    try:
        curses.init_color(curses.COLOR_BLACK, 84,  84,   84)
    except:
        pass
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN) #256
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) #512
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_GREEN) # 768
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK) # 1024
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK) # 2048
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK) # 1536
    print_top_bar(screen, test)

def print_top_bar(screen, test):
    """
    Print the top bar with the name of the program, the time and the name of the file
    Args:
        screen: curses screen
        test: name of the file
    """
    clear_line(screen, 0)
    width = get_dimension(screen)[1]
    screen.addstr(0,width//2 - len(test)//2, f" {test} " , WHITE_CYAN | BOLD)

    screen.refresh()

def get_dimension(screen):
    """
    Get the dimensions of the screen
    Args:
        screen: curses screen
    Returns:
        height, width
    """
    return screen.getmaxyx()

def end_screen(wpm, accuracy, screen):
    """
    Prints the end screen
    Args:
        wpm: words per minute of the test
        accuracy: accuracy of the test
        screen: curses screen
    """
    screen.clear()
    height, width = get_dimension(screen)
    screen.addstr(height//2 -1 , width//2 - 10, "Test ended!", WHITE_BLACK | BOLD)

    screen.addstr(height//2 + 1, width//2 - 10, "WPM: " + str(wpm), WHITE_BLACK | BOLD)
    screen.addstr(height//2 + 2, width//2 - 10, f"Accuracy: {accuracy:.2f}%", WHITE_BLACK | BOLD)

    screen.addstr(height//2 + 4, width//2 - 10, "Press RETURN to restart", WHITE_BLACK | BOLD)
    screen.addstr(height//2 + 5, width//2 - 10, "Press q to quit", WHITE_BLACK | BOLD)
    screen.refresh()

