import copy

from Exercise import Exercise
from Timer import Timer
from Workout import Workout
class User:

    def __init__(self, name: str, admin: bool, exercises, workouts):
        self.name = name
        self.admin = admin
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
        # Workout data
        self.curr_workout = Workout('', [])
        self.workout_break_exe = Exercise('Break', 0, 6, 2, 0)
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
        # run current exercise
        # if exercise not in progress or started update display and return
        if not self.exe_running and not self.curr_exe_started:
            # load current values into the timer, for display
            if self.curr_exe.delay > 0:
                self.curr_exe_mode = 'Delay'
                self.my_timer.active_time = self.curr_exe.delay
            else:
                self.curr_exe_mode = 'Ready'
                self.my_timer.active_time = self.curr_exe.worktime
            # update timer dispaly
            self.my_timer.calculate_time()
            return -1
        # if exercise is not valid - worktime > 0, number of rounds > 0 return
        if not self.curr_exe_valid:
            return -2
        self.curr_exe_started = True
        # Exercise running - check if delay is present
        if self.curr_exe.delay > 0 and not self.curr_exe_delay_done:
            # Run delay
            self.curr_exe_mode = 'Delay'
            # Start timer
            if self.my_timer.timing_function(self.curr_exe.delay, self.exe_running):
                self.curr_exe_delay_done = True
                self.my_timer.reset()
        # If delay not present or finished run proper exercise
        else:
            # check if exercise not finished
            if self.curr_exe_round <= self.curr_exe.num_rounds:
                if not self.curr_exe_break_on and self.curr_exe.worktime > 0:
                    # Work mode
                    self.curr_exe_mode = 'Work'
                    # Start timer
                    if self.my_timer.timing_function(self.curr_exe.worktime, self.exe_running):
                        self.curr_exe_break_on = True
                        self.my_timer.reset()
                else:
                    # Break mode
                    # No break on the last round
                    if self.curr_exe_round == self.curr_exe.num_rounds:
                        # End of exercise
                        self.curr_exe_finished = True
                    else:
                        if self.curr_exe.breaktime > 0:
                            self.curr_exe_mode = 'Break'
                        # Start timer
                        if self.my_timer.timing_function(self.curr_exe.breaktime, self.exe_running):
                            self.curr_exe_break_on = False
                            self.my_timer.reset()
                            self.curr_exe_round += 1

    def reset_exe(self):
        # reset current exercise to start values
        #self.curr_exe_mode = 'Ready'
        self.curr_exe_delay_done = False
        self.curr_exe_break_on = False
        self.curr_exe_round = 1
        self.exe_running = False
        self.my_timer.reset()
        self.curr_exe_started = False
        self.curr_exe_finished = False

    def reset_workout(self):
        # reset current workout to start values
        self.curr_workout_started = False
        self.curr_workout_finished = False
        self.curr_workout_break = False

    def check_exe(self):
        # return true if exercise is valid: worktime > 0, number of rounds > 0 return
        if self.curr_exe.num_rounds > 0 and (self.curr_exe.worktime > 0 or self.curr_exe.breaktime > 0):
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
                if self.curr_workout_break:
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
            self.exercises[name].worktime = inputs[1]
            self.exercises[name].breaktime = inputs[2]
            self.exercises[name].num_rounds = inputs[3]
            self.exercises[name].delay = inputs[4]
        else:
            self.exercises[name] = Exercise(*inputs)

    def delete_exercise(self, exe_name):
        # Delete exercise with given name if present
        if exe_name in self.exercises:
            self.exercises.pop(exe_name)


















