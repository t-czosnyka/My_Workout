from Timer import Timer


class Exercise:
    # class representing single exercise data: exercise name, delay before start, length of work time in second,
    # length of break time in seconds, number of rounds
    def __init__(self, name='', worktime_sec=0, breaktime_sec=0, num_rounds=0, delay_sec=0):
        self.name = name
        self.worktime_sec = worktime_sec
        self.breaktime_sec = breaktime_sec
        self.num_rounds = num_rounds
        self.delay_sec = delay_sec

    def __str__(self):
        return self.name + f" :worktime:{self.worktime_sec}, breaktime:{self.breaktime_sec}, rounds:{self.num_rounds}, " \
                           f"delay:{self.delay_sec}"


def encode_exercise(o: Exercise):
    # encode exercise data as dict to export
    return {'name': o.name, 'worktime_sec': o.worktime_sec, 'breaktime_sec': o.breaktime_sec,
            'num_round': o.num_rounds, 'delay_sec': o.delay_sec}


class ExerciseProcessor:
    # class processing exercise signals in real time
    def __init__(self):
        self.current_exercise = Exercise('', 0, 0, 0, 0)
        self.exercise_running = False
        self.current_exercise_mode = 'Ready'
        self.delay_finished = False
        self.current_round = 1
        self.exercise_valid = False
        self.exercise_started = False
        self.exercise_finished = False
        self.work_finished = False
        self.break_finished = False
        self.my_timer = Timer()
        self.req_play_sound = False
        self.current_exercise_valid = False

    def start_exercise(self):
        # start timer
        self.exercise_running = True

    def pause_exercise(self):
        # pause timer
        self.exercise_running = False

    def load_exercise(self, exercise: Exercise):
        if not self.exercise_started:
            self.current_exercise = exercise

    def main(self):
        # run current exercise: delay->(work->break)*n-1->work, n - number of rounds, no break in the last round
        self.req_play_sound = False
        # if exercise not in progress or finished update display and return
        if not self.exercise_running and not self.exercise_started or self.exercise_finished:
            self.update_display()
            self.check_exercise()
            self.exercise_finished = False
            return
        self.exercise_started = True
        # Exercise running select mode Delay/Work/Break
        delay = self.current_exercise.delay_sec > 0 and not self.delay_finished
        # Delay Mode
        if delay:
            self.current_exercise_mode = 'Delay'
            # Start timer
            if self.my_timer.countdown_timer(self.current_exercise.delay_sec, self.exercise_running, False):
                # Timer finished
                self.delay_finished = True
                self.my_timer.reset()
        # Work Mode
        elif not self.work_finished and self.current_exercise.worktime_sec > 0:
            self.current_exercise_mode = 'Work'
            # Start timer
            # Request play sound at the beginning of work time
            if not self.my_timer.timer_started:
                self.req_play_sound = True
            if self.my_timer.countdown_timer(self.current_exercise.worktime_sec, self.exercise_running, True):
                # Timer finished
                self.work_finished = True
                self.my_timer.reset()
                # Request play sound at the end of work time
                self.req_play_sound = True
        # Break Mode
        else:
            self.current_exercise_mode = 'Break'
            # Start timer
            if self.my_timer.countdown_timer(self.current_exercise.breaktime_sec, self.exercise_running, False):
                # Timer finished
                self.break_finished = True
                self.my_timer.reset()
        # Round finished, reset marker and increment number of rounds, not for delay
        if not delay and (self.work_finished or self.current_exercise.worktime_sec == 0) and\
                (self.break_finished or self.current_exercise.breaktime_sec == 0 or
                 self.current_round == self.current_exercise.num_rounds):
            self.work_finished = False
            self.break_finished = False
            self.current_round += 1
        # End of exercise, special condition if worktime = 0
        if self.current_round > self.current_exercise.num_rounds or\
                self.current_exercise.worktime_sec == 0 and self.current_round == self.current_exercise.num_rounds:
            self.current_round = self.current_exercise.num_rounds
            self.exercise_finished = True
            self.reset_exercise()

    def update_display(self):
        # updating display for fluid visualisation when exercise is not yet started
        # load current values into the timer, for display
        if self.current_exercise.delay_sec > 0:
            self.current_exercise_mode = 'Delay'
            self.my_timer.active_time_sec = self.current_exercise.delay_sec
        elif self.current_exercise.worktime_sec > 0:
            self.current_exercise_mode = 'Work'
            self.my_timer.active_time_sec = self.current_exercise.worktime_sec
        else:
            self.current_exercise_mode = 'Break'
            self.my_timer.active_time_sec = self.current_exercise.breaktime_sec
        # update timer display
        self.my_timer.update_time_display()

    def reset_exercise(self):
        # reset current exercise to start values
        self.delay_finished = False
        self.work_finished = False
        self.break_finished = False
        self.current_round = 1
        self.exercise_running = False
        self.my_timer.reset()
        self.exercise_started = False
        #self.exercise_finished = False

    def check_exercise(self):
        # return true if exercise is valid: worktime > 0, number of rounds > 0 return
        if self.current_exercise.num_rounds > 0 and (self.current_exercise.worktime_sec > 0 or
                                                     (self.current_exercise.breaktime_sec > 0 and self.current_exercise.num_rounds > 1)):
            self.current_exercise_valid = True
        else:
            self.current_exercise_valid = False
