import copy
from Exercise import Exercise, encode_exercise
from Workout import Workout, encode_workout


class User:
    # User class stores and handles editing of user exercise and workout data
    def __init__(self, name: str, exercises: dict, workouts: dict, email: str,):
        self.name = name
        self.email = email
        self.exercises = exercises
        self.workouts = workouts
        # Interface to Gui
        self.req_workout_update = False

    # def main_run(self):
    #     # main user function evaluate signals from exercise/workout and communicate with gui
    #     # run exercise and workout functions
    #     self.exercise_processor.main()
    #     self.run_workout()
    #     # evaluate outputs of these functions
    #     if self.exercise_processor.exercise_finished:
    #         self.exercise_processor.reset_exercise()
    #         # exercise finished in single exercise mode
    #         if not self.curr_workout_started:
    #             self.req_exercise_finish_to_gui = True
    #             self.exercise_processor.update_display()
    #         # exercise finished in workout mode -> start next exercise
    #         elif not self.curr_workout_finished:
    #             self.req_select_next_exe = True
    #         # workout finished
    #         else:
    #             self.req_workout_finish_to_gui = True
    #             self.reset_workout()

    def save_exercise(self, inputs: list):
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
        if workout_name == '':
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

    def get_workout(self, workout_name):
        # Return workout with requested name if it exists
        if workout_name in self.workouts:
            return self.workouts[workout_name]
        else:
            return None

    def get_exercise(self, exercise_name):
        # Return exercise with requested name if it exists
        if exercise_name in self.exercises:
            return self.exercises[exercise_name]
        else:
            return None

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

    def encode_exercises(self):
        # return dictionary with list of all exercises to be written in JSON file
        data = {'exercises': []}
        for exe in list(self.exercises.values()):
            data['exercises'].append(encode_exercise(exe))
        return data

    def encode_workouts(self):
        # return dictionary with list of all workouts to be written in JSON file
        data = {'workouts': []}
        for work in list(self.workouts.values()):
            data['workouts'].append(encode_workout(work))
        return data

    def req_workout_update_set(self):
        self.req_workout_update = True

    def req_workout_update_reset(self):
        self.req_workout_update = False

    def req_select_next_exe_reset(self):
        self.req_select_next_exe = False






















