import copy

from Exercise import Exercise
from Timer import Timer
from Workout import Workout
class User:

    def __init__(self, name: str, email, password, exercises, workouts):
        self.name = name
        self.email = email
        self.password = password
        self.exercises = exercises  # exercises data
        self.workouts = workouts    # workouts data
        self.my_timer = Timer()
        # Exercise data
        self.curr_exe = Exercise('', 0, 0, 0, 0)
        self.exe_running = False            #start/pause
        self.curr_exe_mode = 'Ready'
        self.curr_exe_delay_done = False
        self.curr_exe_round = 1
        self.curr_exe_break_on = False
        self.curr_exe_valid = False
        self.curr_exe_started = False
        self.curr_exe_finished = False
        self.exe_work_finish = False
        self.exe_break_finish = False
        # Workout data
        self.curr_workout = Workout('', [], 0)
        self.workout_break_exe = Exercise('', 0, 0, 2, 0)
        self.curr_workout_started = False
        self.curr_workout_finished = False
        self.curr_workout_break = False

    def start_run(self):
        # start timer
        self.exe_running = True

    def stop_run(self):
        # pause timer
        self.exe_running = False

    def run_exe(self):
        # run current exercise: delay->(work->break)*n-1->work, n - number of rounds, no break in last round
        # if exercise not in progress or finished update display and return
        if not self.exe_running and not self.curr_exe_started or self.curr_exe_finished:
            self.update_display()
            return -1
        # if exercise is not valid - worktime > 0, number of rounds > 0 or finished return
        if not self.curr_exe_valid:
            return -2
        self.curr_exe_started = True
        # Exercise running select mode Delay/Work/Break
        delay = self.curr_exe.delay_sec > 0 and not self.curr_exe_delay_done
        # Delay Mode
        if delay:
            self.curr_exe_mode = 'Delay'
            # Start timer
            if self.my_timer.timing_function(self.curr_exe.delay_sec, self.exe_running):
                self.curr_exe_delay_done = True
                self.my_timer.reset()
        # Work Mode
        elif not self.exe_work_finish and self.curr_exe.worktime_sec > 0:
            self.curr_exe_mode = 'Work'
            # Start timer
            if self.my_timer.timing_function(self.curr_exe.worktime_sec, self.exe_running):
                self.my_timer.reset()
                self.exe_work_finish = True
        # Break Mode
        else:
            self.curr_exe_mode = 'Break'
            # Start timer
            if self.my_timer.timing_function(self.curr_exe.breaktime_sec, self.exe_running):
                self.my_timer.reset()
                self.exe_break_finish = True
        # Round finished, reset marker and increment number of rounds, not for delay
        if not delay and (self.exe_work_finish or self.curr_exe.worktime_sec == 0) and\
                (self.exe_break_finish or self.curr_exe.breaktime_sec == 0 or
                 self.curr_exe_round == self.curr_exe.num_rounds):
            self.exe_work_finish = False
            self.exe_break_finish = False
            self.curr_exe_round += 1
        # End of exercise, special condition if worktime = 0
        if self.curr_exe_round > self.curr_exe.num_rounds or\
                self.curr_exe.worktime_sec == 0 and self.curr_exe_round == self.curr_exe.num_rounds:
            self.curr_exe_round = self.curr_exe.num_rounds
            self.curr_exe_finished = True

    def update_display(self):
        # updating dispaly for fluid visualisation
        # load current values into the timer, for display
        if self.curr_exe.delay_sec > 0:
            self.curr_exe_mode = 'Delay'
            self.my_timer.active_time = self.curr_exe.delay_sec
        elif self.curr_exe.worktime_sec > 0:
            self.curr_exe_mode = 'Work'
            self.my_timer.active_time = self.curr_exe.worktime_sec
        else:
            self.curr_exe_mode = 'Break'
            self.my_timer.active_time = self.curr_exe.breaktime_sec
        # update timer display
        self.my_timer.calculate_time()

    def reset_exe(self):
        # reset current exercise to start values
        self.curr_exe_delay_done = False
        self.curr_exe_break_on = False
        self.curr_exe_round = 1
        self.exe_running = False
        self.my_timer.reset()
        self.curr_exe_started = False
        self.curr_exe_finished = False
        self.exe_work_finish = False
        self.exe_break_finish = False

    def reset_workout(self):
        # reset current workout to start values
        self.curr_workout_started = False
        self.curr_workout_finished = False
        self.curr_workout_break = False

    def check_exe(self):
        # return true if exercise is valid: worktime > 0, number of rounds > 0 return
        if self.curr_exe.num_rounds > 0 and (self.curr_exe.worktime_sec > 0 or
                                             (self.curr_exe.breaktime_sec > 0 and self.curr_exe.num_rounds > 1)):
            self.curr_exe_valid = True
        else:
            self.curr_exe_valid = False

    def load_next_exercise(self):
        # load next exercise from workout if available
        if len(self.curr_workout.exercises) > 0:
            next_exe_name = self.curr_workout.exercises.pop(0)[0]
            # check if this exercise is available
            if next_exe_name in self.exercises:
                # Load first exercise from current workout and start workout
                self.curr_exe = copy.deepcopy(self.exercises[next_exe_name])
                return True
        return False

    def start_workout(self):
        # start current workout
        # return True if exercise was loaded
        if not self.curr_workout_started:
            self.reset_exe()
            if self.load_next_exercise():
                self.curr_workout_started = True
                self.curr_workout_break = True
                self.workout_break_exe.breaktime_sec = self.curr_workout.extra_break_sec
        return self.curr_workout_started

    def run_workout(self):
        # continuous function to run current workout
        if not self.curr_workout_started:
            return
        # curr_exe_finished set by run_exe function
        if self.curr_exe_finished:
            # check if there are more exercises
            if len(self.curr_workout.exercises) > 0:
                # Break between exercises
                if self.curr_workout_break and self.curr_workout.extra_break_sec > 0:
                    print("workout break")
                    self.curr_exe = copy.deepcopy(self.workout_break_exe)
                    self.curr_workout_break = False
                # Next exercise
                else:
                    if self.load_next_exercise():
                        print("New exercise")
                        self.curr_workout_break = True
            else:
                # End of workout
                print("end workout")
                self.curr_workout_finished = True

    def load_workout(self, selected_name):
        # Load selected workout into curr_workout
        # check if selected workout exists
        if selected_name in self.workouts:
            self.curr_workout = copy.deepcopy(self.workouts[selected_name])
            return True
        return False

    def save_exercise(self, inputs):
        # Create or update exercise object based on input from Gui
        name = inputs[0]
        if name in self.exercises:
            self.exercises[name].worktime_sec = inputs[1]
            self.exercises[name].breaktime_sec = inputs[2]
            self.exercises[name].num_rounds = inputs[3]
            self.exercises[name].delay_sec = inputs[4]
        else:
            self.exercises[name] = Exercise(*inputs)

    def delete_exercise(self, exe_name):
        # Delete exercise with given name if present
        if exe_name in self.exercises:
            self.exercises.pop(exe_name)


















