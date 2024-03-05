import csv
import os
from datetime import date

def get_history_file():
    """
    Get the history file
    Returns:
        string: path to the history file
    """
    # get the ~/.cache/typingtest directory
    cache = os.path.expanduser("~/.cache/typingtest")
    if not os.path.exists(cache):
        os.makedirs(cache)
        with open (os.path.join(cache, "history.csv"), "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Test", "WPM", "Accuracy"])
    # get the history file
    history = os.path.join(cache, "history.csv")
    return history

def write_history(test, wpm, accuracy):
    """
    Write the history to the history file
    Args:
        time: type of test
        wpm: words per minute
        accuracy: accuracy in percentage
    """
    check_cache_size()
    history = get_history_file()
    with open(history, mode="a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([date.today(), test, wpm, f"{accuracy:.2f}%"])

def check_cache_size():
    """
    Check if the cache file is too big
    Returns:
        bool: True if the file was too big and was truncated
    """
    history = get_history_file()
    if os.path.exists(history):
        size = os.path.getsize(history)
        if size > 10000:
            with open(history, "r") as f:
                lines = f.readlines()
            with open(history, "w") as f:
                writer = csv.writer(f)
                writer.writerows(lines[100:])
            return True

def print_history():
    """
    Print the history of the tests
    """
    history = get_history_file()
    if not os.path.exists(history):
        print("No history found")
    else:
        with open(history, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
