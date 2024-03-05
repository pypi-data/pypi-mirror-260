import random
import os

def read_file(filename):
    '''
    Reads the file and returns a a string of all the words
    Args:
        filename: name of the file
    Returns:
        string of words separated by a space
    '''
    curr_dir = os.path.dirname(__file__)
    file = open (f'{curr_dir}/words/{filename}', "r")
    words = file.read().replace("\n", " ")
    return words

def get_text(filename, number_of_words = 250):
    '''
    Takes the words file and returns a string of words
    Args:
        filename: name of the file
        window_width: typing window width
        number_of_words: number of words to be returned
    Returns:
        string of words, separated by a space
    '''
    words = read_file(filename).split()
    text = ""
    for i in range(number_of_words):
        text += words[random.randint(0, len(words)-1)] + " "
    return text, text.split()

def wrap_text(window_width, text_appended, prev_text = ""):
    """
    Wraps the text to fit the window width
    Args:
        window_width: width of the window
        text_appended: string to be wrapped
        prev_text: previous text
    Returns:
        string of words, separated by a space
    """
    words = text_appended.split()
    for i in range(len(words)):
        line_width = (len(prev_text) % window_width ) + (len(words[i]) + 1)
        if line_width > window_width :
            prev_text += " " * (window_width - (len(prev_text) % window_width))
        prev_text += words[i] + " "
    return prev_text

def print_text(text, start, end, mode, window):
    """
    Prints string on the window
    Args:
        text: string to be printed
        start: start index of the string
        end: end index of the string
        mode: curses mode to be used
        window: window to be printed on
    
    """
    window.addstr(2,0, text[start:end], mode)

def print_char(char, y, x, mode, window):
    """
    Prints a single character on the window
    Args:
        char: character to be printed
        y: y position of the character
        x: x position of the character
        mode: curses mode to be used
        window: window to be printed on
    """
    window.addch(y, x, char, mode)

def clear_line (window, line):
    """
    Clears a line on the window
    Args:
        window: window to be cleared
        line: y position of the line
    """
    height, width = window.getmaxyx()
    window.addstr(line, 0, " " * width)
