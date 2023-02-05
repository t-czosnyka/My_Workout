import copy

from Exercise import Exercise
from Timer import Timer
from Workout import Workout
class User:

    def __init__(self, name: str, admin: bool, exercises, workouts):
        self.name = name
        self.admin = admin
        self.exercises = exercises
        self.workouts = workouts
        self.queue = []
        self.my_timer = Timer()
        self.delay_done = False
        self.curr_round = 1
        self.break_on = False
        self.running = False            #start/pause
        self.mode = 'Ready'
        self.curr_exe = Exercise('',0,0,0,0)
        self.workout_break_exe = Exercise('Break', 0, 6, 2, 0)
        self.valid_exe = False
        self.curr_workout = Workout('',[])

    def start_run(self):
        # start timer
        self.running = True

    def stop_run(self):
        # pause timer
        self.running = False

    def run_exe(self):
        # run current exercise
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

                if not self.break_on and self.curr_exe.worktime > 0:
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
                        #End of exercise
                        self.curr_exe.finished = True

                    else:
                        if self.curr_exe.breaktime > 0:
                            self.mode = 'Break'
                        # Start timer
                        if self.my_timer.timing_function(self.curr_exe.breaktime, self.running):
                            self.break_on = False
                            self.my_timer.reset()
                            self.curr_round += 1
    def reset_exe(self):
        # reset current exercise to start values
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
        if self.curr_exe.num_rounds > 0 and (self.curr_exe.worktime > 0 or self.curr_exe.breaktime > 0):
            self.valid_exe = True
        else:
            self.valid_exe = False

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
        if not self.curr_workout.started:
            self.reset_exe()
            if self.load_next_exercise():
                self.curr_workout.start_workout()
        return self.curr_workout.started

    def run_workout(self):
        # continuous function to run current workout
        if not self.curr_workout.started:
            return
        # curr_exe.finished set by run_exe function
        if self.curr_exe.finished:
            # Load next exercise if current is finished
            self.curr_workout.set_exe_finished()
            # Break between exercises
            if self.curr_workout.work_break:
                print("workout break")
                self.curr_exe = copy.deepcopy(self.workout_break_exe)
            # Next exercise
            else:
                if self.load_next_exercise():
                    print("New exercise")
                else:
                    # End of workout
                    print("end workout")
                    self.curr_workout.finish_workout()
            self.reset_exe()

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


















