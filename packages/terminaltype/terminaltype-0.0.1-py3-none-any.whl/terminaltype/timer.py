import threading
import time

class Timer:
    def __init__(self, time=60):
        self.timer_running = False
        self.time = time
        self.curr_time = self.time
        self.timer_thread = threading.Thread(target=self.timer)

    def set_time(self, time):
        if not self.timer_running:
            self.time = time

    def reset(self):
        self.timer_thread = threading.Thread(target=self.timer)
        self.curr_time = self.time
        self.timer_running = False

    def start(self):
        self.curr_time = self.time
        self.timer_running = True
        self.timer_thread.start()

    def stop(self):
        self.timer_running = False

    def timer(self):
        while self.timer_running and self.curr_time > 0:
            self.curr_time -= 1
            time.sleep(1)
        self.stop()

    def get_time(self):
        return self.curr_time

    def running(self):
        return self.timer_running
