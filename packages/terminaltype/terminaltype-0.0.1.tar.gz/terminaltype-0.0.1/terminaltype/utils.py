from terminaltype.window import get_dimension

def calculate_wpm(correct_words, time):
    """
    Calculate the words per minute
    Args:
        correct_words: number of correct words
        time: time taken to type the words
    Returns:
        int: words per minute
    """
    return correct_words // (time / 60)

def calculate_accuracy(text, curr_string, cursor_position):
    """
    Calculate the accuracy
    Args:
        text: string to be compared
        curr_string: string to compare
        cursor_position: position of the cursor
    Returns:
        int: accuracy
    """
    return sum(1 for x, y in zip(text, curr_string) if x == y ) * 100 / cursor_position

def calculate_typing_window_dimensions(screen) -> tuple:
    """
    Get the dimentions of the typing window
    Args:
        screen: curses screen
    Returns:
        tuple: (height, width)
    """
    height, width = get_dimension(screen)
    if (width < 90):
        return (height-3, width)
    elif (width > 160):
        return (height-3, width-40)
    else:
        return (height-3, width-30)
