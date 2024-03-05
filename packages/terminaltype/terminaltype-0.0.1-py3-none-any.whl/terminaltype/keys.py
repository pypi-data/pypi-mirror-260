import curses.ascii

def key_is_alphanumeric(key:str) -> bool:
    if not isinstance(key, str) or len(key) > 1:
        return False
    return key.isalnum() and not key_is_return(key)

def key_is_space(key) -> bool:
    if not isinstance(key, str):
        return False
    return key == " "

def key_is_backspace(key) -> bool:
    if key in ("KEY_BACKSPACE", "\b", "\x7f"):
        return True
    return key in (curses.KEY_BACKSPACE, curses.KEY_DC)

def key_is_ctrl_backspace(key) -> bool:
    return key == curses.ascii.DEL and curses.keyname(key) == "^?"
 
def key_is_escape(key) -> bool:
    if isinstance(key, str):
        return ord(key) == curses.ascii.ESC
    return False

def key_is_return(key) -> bool:
    return key == curses.ascii.NL or key == curses.ascii.CR or key == '\n'

def key_is_resize(key) -> bool:
    return key == curses.KEY_RESIZE
