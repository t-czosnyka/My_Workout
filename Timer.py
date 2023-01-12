from time import perf_counter
class Timer:

    def __init__(self):
        self.active_time = 0
        self.timer_started = False
        self.last_time = None

    def timing_function(self, start_time: int, start: bool, reset: bool):
        # start time in seconds

        if not self.timer_started or reset:
            self.active_time = float(start_time)
            self.timer_started = False
        if start and self.active_time > 0.0:
            if not self.timer_started:
                self.timer_started = True
                self.last_time = perf_counter()
            diff = perf_counter() - self.last_time
            self.last_time = perf_counter()
            self.active_time -= diff
            self.active_time = self.active_time if self.active_time >= 0 else 0.0
            mins = int(self.active_time // 60)
            sec = int((self.active_time - mins * 60) // 1)
            csec = int(round((self.active_time - mins * 60 - sec) % 1, 2) * 100)
            csec = csec if csec <= 99 else 99
            print(f"{mins}:{sec}:{csec}", end=' ')