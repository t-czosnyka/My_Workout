from Exercise import Exercise
from Timer import Timer
class User:

    def __init__(self, name: str, admin: bool, exercises):
        self.name = name
        self.admin = admin
        self.exercises = exercises
        #self.exercises['test']=Exercise('test',0,0,0,0)
        self.workouts = {}
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
        # start current exercise
        # if exercise not in progress or started update display and return
        if not self.running and not self.curr_exe.started:
            # load current values into the timer, for display
            if self.curr_exe.delay > 0:
                self.mode = 'Delay'
                self.my_timer.active_time = self.curr_exe.delay
            else:
                self.mode = 'Ready'
                self.my_timer.active_time = self.curr_exe.worktime
            # update timer dispaly
            self.my_timer.calculate_time()
            return -1
        # if exercise is not valid - worktime > 0, number of rounds > 0 return
        if not self.valid_exe:
            return -2
        self.curr_exe.started = True
        # Exercise running - check if delay is present
        if self.curr_exe.delay > 0 and not self.delay_done:
            # Run delay
            self.mode = 'Delay'
            # Start timer
            if self.my_timer.timing_function(self.curr_exe.delay, self.running):
                self.delay_done = True
                self.my_timer.reset()
        # If delay not present or finished run proper exercise
        else:
            # check if exercise not finished
            if self.curr_round <= self.curr_exe.num_rounds:

                if not self.break_on:
                    # Work mode
                    self.mode = 'Work'
                    # Start timer
                    if self.my_timer.timing_function(self.curr_exe.worktime, self.running):
                        self.break_on = True
                        self.my_timer.reset()
                else:
                    # Break mode
                    # No break on the last round
                    if self.curr_round == self.curr_exe.num_rounds:
                        self.curr_exe.finished = True

                    else:
                        self.mode = 'Break'
                        # Start timer
                        if self.my_timer.timing_function(self.curr_exe.breaktime, self.running):
                            self.break_on = False
                            self.my_timer.reset()
                            self.curr_round += 1
    def reset_exe(self):
        # reset exercise to start values
        self.mode = 'Ready'
        self.delay_done = False
        self.break_on = False
        self.curr_round = 1
        self.running = False
        self.my_timer.reset()
        self.curr_exe.started = False
        self.curr_exe.finished = False

    def check_exe(self):
        # return true if exercise is valid: worktime > 0, number of rounds > 0 return
        if self.curr_exe.num_rounds > 0 and self.curr_exe.worktime > 0:
            self.valid_exe = True
        else:
            self.valid_exe = False














