import time
from time import perf_counter

class Timer:

    def __init__(self):
        self.active_time = 0
        self.timer_started = False
        self.last_time = None
        self.finish = False
        self.time_str = '00:00:00'

    def timing_function(self, start_time: int, start: bool):
        # start time in seconds
        #time.sleep(0.1)
        if not self.timer_started and not self.finish:
            self.active_time = float(start_time)
            self.timer_started = False
        if not start and self.timer_started:
            self.last_time = perf_counter()
        if start and self.active_time > 0.0:
            if not self.timer_started:
                self.timer_started = True
                self.last_time = perf_counter()
            diff = perf_counter() - self.last_time
            self.last_time = perf_counter()
            self.active_time -= diff
            self.active_time = self.active_time if self.active_time >= 0 else 0.0
            self.calculate_time()
        if self.active_time == 0.0:
            self.timer_started = False
            self.finish = True
        return self.finish

    def reset(self):
        #reset timer
        self.active_time = 0
        self.timer_started = False
        self.finish = False
        self.time_str = '00:00:00'

    def calculate_time(self):
        # Convert active time into string
        # Divide into mins, sec, csec
        mins = int(self.active_time // 60)
        sec = int((self.active_time - mins * 60) // 1)
        csec = int(round((self.active_time - mins * 60 - sec) % 1, 2) * 100)
        csec = csec if csec <= 99 else 99
        # Create string
        mins_str = (str(mins) if mins >= 10 else '0' + str(mins))
        sec_str = (str(sec) if sec >= 10 else '0' + str(sec))
        csec_str = (str(csec) if csec >= 10 else '0' + str(csec))
        self.time_str = mins_str + ":" + sec_str + ":" + csec_str
        # print(f"{mins}:{sec}:{csec}", end=' ')
