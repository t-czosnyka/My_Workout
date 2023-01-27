
from Exercise import Exercise
from Timer import Timer
class User:

    def __init__(self, name: str, admin: bool, exercises):
        self.name = name
        self.admin = admin
        self.exercises = exercises
        #self.exercises['test']=Exercise('test',0,0,0,0)
        self.workouts = []
        self.queue = []
        self.my_timer = Timer()
        self.delay_done = False
        self.curr_round = 1
        self.break_on = False
        self.running = False            #start/pause
        self.mode = 'Ready'
        self.curr_exe = Exercise('',0,0,0,0)
        self.valid_exe = False


    def run_exe(self):

        if not self.valid_exe:
            return -1
        if not self.running and not self.curr_exe.started:
            return -2
        if self.curr_exe.delay > 0 and not self.delay_done:
            self.mode = 'Delay'
            self.curr_exe.started = True
            if self.my_timer.timing_function(self.curr_exe.delay, self.running):
                self.delay_done = True
                self.my_timer.reset()
        else:
            self.curr_exe.started = True
            if self.curr_round <= self.curr_exe.num_rounds:
                if not self.break_on:
                    self.mode = 'Work'
                    if self.my_timer.timing_function(self.curr_exe.worktime, self.running):
                        self.break_on = True
                        self.my_timer.reset()
                else:
                    if self.curr_round == self.curr_exe.num_rounds:
                        self.curr_exe.finished = True
                        #self.mode = 'Finished'

                    else:
                        self.mode = 'Break'
                        if self.my_timer.timing_function(self.curr_exe.breaktime, self.running):
                            self.break_on = False
                            self.my_timer.reset()
                            self.curr_round += 1
    def reset_exe(self):
        self.mode = 'Ready'
        self.delay_done = False
        self.break_on = False
        self.curr_round = 1
        self.running = False
        self.my_timer.reset()
        self.curr_exe.started = False
        self.curr_exe.finished = False

    def check_exe(self):
        if self.curr_exe.num_rounds > 0 and self.curr_exe.worktime > 0:
            self.valid_exe = True
        else:
            self.valid_exe = False














