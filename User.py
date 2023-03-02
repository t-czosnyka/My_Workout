from Exercise import Exercise, encode_exercise
from Workout import Workout, encode_workout


class User:
    # User class stores and handles editing of user data
    def __init__(self, name: str, exercises: dict, workouts: dict, email: str,):
        self.name = name
        self.email = email
        self.exercises = exercises
        self.workouts = workouts
        # Interface to Gui
        self.req_workout_update = False

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

    def update_user_data(self, data):
        # update user data if changed
        self.email = data[0]

    def save_workout(self, workout_name: str, exercises: list, extra_break_sec: int):
        # save workout with given data into user data
        # workout name cannot be empty
        if workout_name == '':
            return
        # check if workout already exists
        if workout_name in self.workouts:
            # update existing workout
            self.workouts[workout_name].extra_break_sec = extra_break_sec
            # clear current exercise list
            self.workouts[workout_name].exercises.clear()
        else:
            # create new workout
            self.workouts[workout_name] = Workout(workout_name, [], extra_break_sec)
        # add exercises
        for exe_name in exercises:
            self.workouts[workout_name].exercises.append(exe_name)

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
        # return int of string_var or 0 if empty
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
