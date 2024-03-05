import curses
import sys
from terminaltype.window import (
    init_screen,
    print_top_bar,
    end_screen,
    get_dimension
)
from terminaltype.text import (
    get_text,
    print_text,
    print_char,
    clear_line,
    wrap_text
)
from terminaltype.keys import *
from terminaltype.utils import *
from terminaltype.colors import *
from terminaltype.timer import * # type: ignore
from terminaltype.history import(
    write_history
)
from terminaltype.arguments import get_args


class TypingTest:

    def __init__(self):
        # String with the words and the number of words
        self.number_of_words = 500
        self.correct_words = 0
        self.text = ""
        self.backup_text = ""

        # Screen dimentions
        self.screen_height = 0
        self.screen_width = 0

        # Typing window dimentions
        self.typing_window_height = 0
        self.typing_window_width = 0

        # List of booleans to check if the word is correct
        self.valid = [False] * self.number_of_words

        self.word_position = 0

        # Cursor position in the screen
        self.cursor_position = 0

        # Current Word
        self.curr_word = ""

        # Input text
        self.curr_string = ""

        # Current character
        self.curr_char = ""

        # Current line on the window
        self.curr_line = 1

        # Lines scrolled
        self.lines_scrolled = 0

        # Cursor position of the mistyped keys
        self.mistyped_keys = []
        
        self.wpm = 0
        self.accuracy = 0
        self.time = 0

        self.test, self.time = get_args()
        self.timer = Timer(self.time)

        curses.wrapper(self.main)

    def get_char(self, window):
        """
        Reads a character, returns -1 if no character is pressed for 100ms
        Args:
            window: typing window
        """
        try:
            return window.get_wch()
        except curses.error:
            return -1

    def typing_test(self, window):
        """
        this contains the main loop of the typing test
        Args: 
            window: typing window
        """
        while self.timer.get_time() > 0:

            self.curr_char = self.get_char(window)
         
            if key_is_alphanumeric(self.curr_char) or key_is_space(self.curr_char):
                if not self.timer.running():
                    self.timer.start()
                self.handle_char(self.curr_char)
                self.check_scroll_down()
            elif key_is_backspace(self.curr_char):
                self.erase_char()
            # elif key_is_ctrl_backspace(self.curr_char):
            #     self.erase_word()
            elif key_is_resize(self.curr_char):
                self.resize()
            elif key_is_escape(self.curr_char):
                self.timer.stop()
                sys.exit(0)

            # window.addstr(6,0,"Current Line:" + str(self.curr_line))
            # window.addstr(7,0,"Lines scrolled:" + str(self.lines_scrolled))
            # window.addstr(8,0,"Line:" +str(self.cursor_position // self.typing_window_width + 1))
            # window.addstr(9,0,"                                      ")
            # window.addstr(9,0,"Current Word:"  + str(self.curr_word))
            # window.addstr(10,0,"Length:"  + str(len(self.curr_word)))
            # window.addstr(11,0,"Word Position:" + str(self.word_position))
            # window.addstr(12,0,"Cursor:" + str(self.cursor_position))
            
            self.update_typing_window(self.typing_window, self.timer.get_time())
        self.end_of_test(window)

    def check_scroll_down(self):
        """
        Checks if the window needs to scroll down
        """
        if self.cursor_position % self.typing_window_width == 0 and len(self.curr_string) > 1:
            self.curr_line += 1
        if self.curr_line >= 3 and self.cursor_position % self.typing_window_width == 0:
            self.lines_scrolled += 1

    def handle_char(self, char):
        """
        Handles the input character
        Args:
            char: input character
        """
        self.curr_string += char


        if not self.is_valid_char(char):
            self.mistyped_keys.append(self.cursor_position)
        if self.text[self.cursor_position] == " ":
            if self.is_valid_word(self.curr_word):
                self.valid[self.word_position] = True
            self.end_of_word()
        else:
            self.curr_word += char

        self.cursor_position += 1

    def is_valid_char(self, char):
        """
        Check if the input char is valid
        Args:
            char: input character
        Returns:
            bool: True if the character is valid
        """
        return char == self.text[self.cursor_position]

    def is_valid_word(self, word):
        """
        Check if the current word is valid
        Args:
            word: word to check
        Returns:
            bool: True if the word is valid
        """
        return word == self.words[self.word_position]

    def end_of_word(self):
        """
        Moves the cursor to the beggining of the next word when a space is pressed
        """
        spaces=0
        while self.text[self.cursor_position+1] == " ":
            spaces += 1
            self.cursor_position += 1
        self.curr_string += " " * spaces
        self.word_position += 1
        self.curr_word = ""

    def erase_char(self):
        """
        Erases the last character
        """
        if self.curr_word:
            self.check_scroll_up()
            self.curr_word = self.curr_word[:-1]
            self.curr_string = self.curr_string[:-1]
            self.pop_mystiped_keys()
            self.cursor_position -= 1
        elif self.cursor_position != 0 and not self.valid[self.word_position - 1]:
            self.pop_mystiped_keys()
            self.check_scroll_up()
            self.delete_spaces()
            self.word_position -= 1
            self.curr_word = self.curr_string[-(len(self.words[self.word_position])):]

    def erase_word(self):
        """
        Erases the last word
        """
        if self.curr_word:
            while self.curr_word:
                self.curr_word = self.curr_word[:-1]
                self.curr_string = self.curr_string[:-1]
                self.pop_mystiped_keys()
                self.cursor_position -= 1
        elif self.cursor_position != 0 and not self.valid[self.word_position - 1]:
            self.check_scroll_up()
            self.delete_spaces()
            self.word_position -= 1
            self.curr_word = self.curr_string[-(len(self.words[self.word_position])):]

    def pop_mystiped_keys(self):
        """
        Pops the last mistyped key
        """
        if self.mistyped_keys:
            if self.mistyped_keys[-1] == self.cursor_position - 1:
                self.mistyped_keys.pop()

    def check_scroll_up(self):
            if self.cursor_position % self.typing_window_width == 0 and self.curr_line > 1:
                self.curr_line -= 1
                if self.lines_scrolled > 0:
                    self.lines_scrolled -= 1

    def delete_spaces(self):
        """
        Deletes the spaces at the end of the word
        """
        while self.text[self.cursor_position-1] == " ":
            self.pop_mystiped_keys()
            self.curr_string = self.curr_string[:-1]
            self.cursor_position -= 1

    def resize(self):
        """
        Resizes the window
        """
        self.screen_height, self.screen_width = get_dimension(self.screen)
        self.typing_window_height, self.typing_window_width = calculate_typing_window_dimensions(self.screen)
        self.screen.resize(self.screen_height, self.screen_width)
        self.typing_window.resize(self.typing_window_height, self.typing_window_width)

        self.resize_text()
        self.curr_line = self.cursor_position // self.typing_window_width + 1
        self.lines_scrolled = self.curr_line - 2 if self.curr_line > 2 else 0

        self.screen.clear()
        self.typing_window.clear()
        print_top_bar(self.screen, self.test)
        self.update_typing_window(self.typing_window, self.timer.get_time())

    def resize_text(self):
        """
        Resizes the text
        """
        text_appended = " ".join(self.text[self.cursor_position+1:].split())
        # not proud of this
        if self.text[self.cursor_position + 1] == " " and self.text[self.cursor_position] != " ":
            self.text = wrap_text(self.typing_window_width, text_appended, self.text[:self.cursor_position+2])
        else:
            self.text = wrap_text(self.typing_window_width, text_appended, self.text[:self.cursor_position+1])

    def update_typing_window(self, window, curr_time):
        """
        Update the typing window, prints the sample and the input text, refreshes the window
        Args:
            window: typing window
            curr_time: current time
        """

        # Print the test text
        print_text(self.text,
                (self.lines_scrolled)*self.typing_window_width,
                (self.lines_scrolled + 3) * self.typing_window_width,
                WHITE_BLACK | DIM,
                window
        )

        # Print the input text
        print_text(self.curr_string,
                (self.lines_scrolled)*self.typing_window_width,
                self.cursor_position,
                WHITE_BLACK | BOLD,
                window
        )

        # Print the mistyped keys
        indexes_to_print = [index for index in self.mistyped_keys if index >= (self.lines_scrolled*self.typing_window_width)  \
            and index >= (self.lines_scrolled * self.typing_window_width) - self.lines_scrolled >= 0]
        for index in indexes_to_print:
            char = "_" if self.text[index] == " " else self.text[index]
            print_char(char,
                       index // self.typing_window_width - self.lines_scrolled + 2,
                       index % self.typing_window_width,
                       RED_BLACK | BOLD,
                       window
                       )

        # Print the time left
        clear_line(window, 0)
        window.addstr(0,0, str(curr_time), GREEN_BLACK | BOLD)

        # Move the cursor to the right position
        window.move(self.curr_line-self.lines_scrolled+1, self.cursor_position % self.typing_window_width)
        window.refresh()

    def end_of_test(self, window):
        """
        Ends the test
        Args:
            window: typing window
        """
        curses.curs_set(0)
        self.timer.stop()
        self.screen.clear()
        self.correct_words = sum(self.valid)
        self.wpm = calculate_wpm(self.correct_words, self.time)
        self.accuracy = calculate_accuracy(self.text, self.curr_string, self.cursor_position)
        write_history(self.test, self.wpm, self.accuracy)
        end_screen(self.wpm, self.accuracy, self.screen) 
        while True:
            char = self.get_char(window)
            if key_is_return(char):
                self.reset_test(window)
            elif char == "q":
                sys.exit(0)

    def reset_test(self,window):
        """
        Resets the test
        Args:
            window: typing window
        """
        self.text, self.words = get_text(self.test, self.number_of_words)
        self.backup_text = self.text
        self.text = wrap_text(self.typing_window_width, self.text)
        self.valid = [False] * self.number_of_words
        self.correct_words = 0
        self.word_position = 0
        self.cursor_position = 0
        self.curr_word = ""
        self.curr_string = ""
        self.curr_char = ""
        self.curr_line = 1
        self.lines_scrolled = 0
        self.mistyped_keys = []
        self.timer.reset()
        self.screen.clear()
        curses.curs_set(2)
        print_top_bar(self.screen, self.test)
        self.typing_test(window)

    def init_typing_window(self, window):
        """
        Initializes the typing window
        Args:
            window: typing window
        """
        window.nodelay(True)
        window.timeout(100)
        print_text(self.text,
                0,
                self.typing_window_width*3,
                WHITE_BLACK | DIM,
                window
        )
        curses.curs_set(2)
        window.move(2,0)
        window.refresh()

    def main(self,screen):
        self.screen = screen
        init_screen(screen, self.test)

        self.screen_height, self.screen_width = get_dimension(screen)
        self.typing_window_height, self.typing_window_width = calculate_typing_window_dimensions(screen)
        self.typing_window = curses.newwin(self.typing_window_height, self.typing_window_width, 5, self.screen_width//2 - self.typing_window_width//2)

        self.text, self.words = get_text(self.test, self.number_of_words)
        self.backup_text = self.text
        self.text = wrap_text(self.typing_window_width, self.text)

        self.init_typing_window(self.typing_window)
        print_top_bar(screen, self.test)
        self.typing_test(self.typing_window)
        curses.endwin()
