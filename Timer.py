from time import perf_counter


class Timer:
    # timer class - used to countdown set amount of time in seconds, after finished countdown reset is required
    # calculating work/break time passed calculate total time of training since user logged in
    def __init__(self):
        self.active_time_sec = 0
        self.timer_started = False
        self.last_time = None
        self.finish = False
        self.work_time_passed_sec = 0
        self.break_time_passed_sec = 0
        self.active_time_str = '00:00:00'
        self.work_time_passed_str = '00:00:00'
        self.break_time_passed_str = '00:00:00'
        self.total_time_passed_str = '00:00:00'

    def countdown_timer(self, set_time_sec: int, start_pause: bool, work: bool):
        # function to be called cyclically in main loop
        # saves last time it was called and calculates the difference between last and current call
        # subtract the difference from set time amount
        # if timer was already started and start input turns to false - countdown pauses
        # work - differentiates between work and break time
        if not self.timer_started and not self.finish:
            # timer not started,
            self.active_time_sec = float(set_time_sec)
        if self.timer_started and not start_pause:
            # timer paused, save current time
            self.last_time = perf_counter()
            return False
        if start_pause and self.active_time_sec > 0.0:
            if not self.timer_started:
                # timer starting, set variable and save current time
                self.timer_started = True
                self.last_time = perf_counter()
            # calculate difference between last call and current call
            diff = perf_counter() - self.last_time
            # save current call as last call
            self.last_time = perf_counter()
            # subtract difference from set time
            self.active_time_sec -= diff
            # add current time as work timer or break time
            if work:
                # work time
                self.work_time_passed_sec += diff
            else:
                # break time
                self.break_time_passed_sec += diff
            # round current timer to zero if it goes below
            self.active_time_sec = self.active_time_sec if self.active_time_sec >= 0 else 0.0
            # convert time values to string
            self.update_time_display()
        if self.active_time_sec == 0.0:
            # countdown finished
            self.timer_started = False
            self.finish = True
        return self.finish

    def reset(self):
        # reset internal timer variables
        self.active_time_sec = 0
        self.timer_started = False
        self.finish = False
        self.active_time_str = '00:00:00'

    @staticmethod
    def time_sec_to_clock_str(time_sec):
        # Convert time into string
        # Divide into minutes, seconds, centiseconds
        mins = int(time_sec // 60)
        sec = int((time_sec - mins * 60) // 1)
        csec = int(round((time_sec - mins * 60 - sec) % 1, 2) * 100)
        csec = csec if csec <= 99 else 99
        # Create string
        mins_str = (str(mins) if mins >= 10 else '0' + str(mins))
        sec_str = (str(sec) if sec >= 10 else '0' + str(sec))
        csec_str = (str(csec) if csec >= 10 else '0' + str(csec))
        return mins_str + ":" + sec_str + ":" + csec_str

    def update_time_display(self):
        # convert all internal time values to strings
        self.active_time_str = self.time_sec_to_clock_str(self.active_time_sec)
        self.work_time_passed_str = self.time_sec_to_clock_str(self.work_time_passed_sec)
        self.break_time_passed_str = self.time_sec_to_clock_str(self.break_time_passed_sec)
        self.total_time_passed_str = self.time_sec_to_clock_str(self.work_time_passed_sec+self.break_time_passed_sec)
