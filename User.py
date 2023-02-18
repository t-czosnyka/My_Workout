import copy

from Exercise import Exercise
from Timer import Timer
from Workout import Workout
class User:

    def __init__(self, name: str, exercises: dict, workouts: dict, email: str,):
        self.name = name
        self.email = email
        self.exercises = exercises  # exercises data
        self.workouts = workouts    # workouts data
        self.my_timer = Timer()
        # Exercise data
        self.current_exercise = Exercise('', 0, 0, 0, 0)
        self.exe_running = False            # start/pause
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
        # Interface to Gui
        self.req_workout_update = False
        self.req_play_sound = False
        self.req_exercise_finish_to_gui = False  # current exercise finished
        self.req_workout_finish_to_gui = False  # current workout finished
        self.req_select_next_exe = False  # req loading next exercise into display

    def main_run(self):
        # main user function evaluate signals from exercise/workout and communicate with gui
        # run exercise and workout functions
        self.run_exe()
        self.run_workout()
        # evaluate outputs of these functions
        if self.curr_exe_finished:
            self.reset_exe()
            # exercise finished in single exercise mode
            if not self.curr_workout_started:
                self.req_exercise_finish_to_gui = True
                self.update_display()
            # exercise finished in workout mode -> start next exercise
            elif not self.curr_workout_finished:
                self.req_select_next_exe = True
                self.start_exercise()
            # workout finished
            else:
                self.req_workout_finish_to_gui = True
                self.reset_workout()

    def start_exercise(self):
        # start timer
        self.exe_running = True

    def pause_exe(self):
        # pause timer
        self.exe_running = False

    def run_exe(self):
        # run current exercise: delay->(work->break)*n-1->work, n - number of rounds, no break in the last round
        # if exercise not in progress or finished update display and return
        if not self.exe_running and not self.curr_exe_started or self.curr_exe_finished:
            self.update_display()
            return -1
        # if exercise is not valid - worktime > 0 or break time > 0 and number of rounds > 0 return
        self.check_exe()
        if not self.curr_exe_valid:
            return -2
        self.curr_exe_started = True
        # Exercise running select mode Delay/Work/Break
        delay = self.current_exercise.delay_sec > 0 and not self.curr_exe_delay_done
        # Delay Mode
        if delay:
            self.curr_exe_mode = 'Delay'
            # Start timer
            if self.my_timer.countdown_timer(self.current_exercise.delay_sec, self.exe_running, False):
                # Timer finished
                self.curr_exe_delay_done = True
                self.my_timer.reset()
        # Work Mode
        elif not self.exe_work_finish and self.current_exercise.worktime_sec > 0:
            self.curr_exe_mode = 'Work'
            # Start timer
            # Request play sound at the beginning of work time
            if not self.my_timer.timer_started:
                self.req_play_sound = True
            if self.my_timer.countdown_timer(self.current_exercise.worktime_sec, self.exe_running, True):
                # Timer finished
                self.exe_work_finish = True
                self.my_timer.reset()
                # Request play sound at the end of work time
                self.req_play_sound = True
        # Break Mode
        else:
            self.curr_exe_mode = 'Break'
            # Start timer
            if self.my_timer.countdown_timer(self.current_exercise.breaktime_sec, self.exe_running, False):
                # Timer finished
                self.exe_break_finish = True
                self.my_timer.reset()
        # Round finished, reset marker and increment number of rounds, not for delay
        if not delay and (self.exe_work_finish or self.current_exercise.worktime_sec == 0) and\
                (self.exe_break_finish or self.current_exercise.breaktime_sec == 0 or
                 self.curr_exe_round == self.current_exercise.num_rounds):
            self.exe_work_finish = False
            self.exe_break_finish = False
            self.curr_exe_round += 1
        # End of exercise, special condition if worktime = 0
        if self.curr_exe_round > self.current_exercise.num_rounds or\
                self.current_exercise.worktime_sec == 0 and self.curr_exe_round == self.current_exercise.num_rounds:
            self.curr_exe_round = self.current_exercise.num_rounds
            self.curr_exe_finished = True

    def update_display(self):
        # updating dispaly for fluid visualisation when exercise is not yet started
        # load current values into the timer, for display
        if self.current_exercise.delay_sec > 0:
            self.curr_exe_mode = 'Delay'
            self.my_timer.active_time_sec = self.current_exercise.delay_sec
        elif self.current_exercise.worktime_sec > 0:
            self.curr_exe_mode = 'Work'
            self.my_timer.active_time_sec = self.current_exercise.worktime_sec
        else:
            self.curr_exe_mode = 'Break'
            self.my_timer.active_time_sec = self.current_exercise.breaktime_sec
        # update timer display
        self.my_timer.update_time_display()

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
        # reload current workout
        self.load_workout(self.curr_workout.name)

    def check_exe(self):
        # return true if exercise is valid: worktime > 0, number of rounds > 0 return
        if self.current_exercise.num_rounds > 0 and (self.current_exercise.worktime_sec > 0 or
                                                     (self.current_exercise.breaktime_sec > 0 and self.current_exercise.num_rounds > 1)):
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
                self.current_exercise = copy.deepcopy(self.exercises[next_exe_name])
                return True
        return False

    def start_workout(self):
        # start current workout, return True if started successfully
        if not self.curr_workout_started:
            self.reset_exe()
            # return True if exercise was loaded
            if self.load_next_exercise():
                self.curr_workout_started = True
                self.curr_workout_break = True
                self.workout_break_exe.breaktime_sec = self.curr_workout.extra_break_sec
        return self.curr_workout_started

    def run_workout(self):
        # continuous function to run current workout
        if not self.curr_workout_started or self.curr_workout_finished:
            return
        # if exercise is finished load next
        # curr_exe_finished set by run_exe function
        if self.curr_exe_finished:
            # check if there are more exercises
            if len(self.curr_workout.exercises) == 0:
                # End of workout if no moe exercises left
                self.curr_workout_finished = True
                return
            # If more exercises are present continue workout
            # Break between exercises
            if self.curr_workout_break and self.curr_workout.extra_break_sec > 0:
                self.current_exercise = copy.deepcopy(self.workout_break_exe)
                self.curr_workout_break = False
            # Next exercise from the list
            elif self.load_next_exercise():
                self.curr_workout_break = True

    def load_workout(self, selected_name):
        # Load selected workout into curr_workout
        # If there are no workouts available -> load empty workout
        if len(self.workouts) == 0:
            self.curr_workout = Workout('', [], 0)
            return True
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
        else:
            return
        # Delete exercise from user workouts and adjust order numbers
        for workout in self.workouts.values():
            shift = 0
            i = 0
            while i < len(workout.exercises):
                # delete exercise if found in workout,
                # increment shift variable to subtract from other exercises order num
                if workout.exercises[i][0] == exe_name:
                    workout.exercises.pop(i)
                    shift += 1
                    continue
                # adjust order number for other exercises if some exercises were already deleted
                elif shift > 0:
                    workout.exercises[i] = (workout.exercises[i][0], workout.exercises[i][1]-shift)
                i += 1


    def change_data(self, data):
        self.email = data[0]

    def save_workout(self, workout_name: str, exercises: list, extra_break_sec: int):
        if workout_name == '' or len(exercises) == 0:
            return
        # check if workout already exists
        if workout_name in self.workouts:
            # update exisitng workout
            self.workouts[workout_name].extra_break_sec = extra_break_sec
        else:
            #create new workout
            self.workouts[workout_name] = Workout(workout_name,[],extra_break_sec)
        # update exercise list
        self.workouts[workout_name].exercises.clear()
        for i, exe_name in enumerate(exercises, 1):
            self.workouts[workout_name].exercises.append((exe_name,i))

    def delete_workout(self, workout_name):
        # Delete workout with given name if present
        if workout_name in self.workouts:
            self.workouts.pop(workout_name)
        else:
            return

    def skip_exercise(self):
        if self.curr_workout_started:
            self.exe_running = False
            self.curr_exe_finished = True

    @staticmethod
    # validating function for time value entry widgets, check if input is digit or is empty, less character than max
    def validate_time_input(entry_input, max_num_char):
        if (entry_input.isdigit() or entry_input == '') and len(entry_input) <= max_num_char:
            return True
        else:
            return False

    @staticmethod
    # validating function for name entry widgets no more than 20 characters
    def validate_name_input(entry_input):
        if len(entry_input) <= 20:
            return True
        else:
            return False

    @staticmethod
    def get_str_var(str_var):
        # return int of stringvar or 0 if empty
        if str_var.get() != '':
            return int(str_var.get())
        else:
            return 0

    def req_workout_update_set(self):
        self.req_workout_update = True

    def req_workout_update_reset(self):
        self.req_workout_update = False

    def req_play_sound_reset(self):
        self.req_play_sound = False

    def req_exercise_finish_to_gui_reset(self):
        self.req_exercise_finish_to_gui = False

    def req_workout_finish_to_gui_reset(self):
        self.req_workout_finish_to_gui = False

    def req_select_next_exe_reset(self):
        self.req_select_next_exe = False

















