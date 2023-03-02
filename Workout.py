from Exercise import Exercise, ExerciseProcessor


class Workout:
    # class holding workout data: name, list of exercises names and additional break
    def __init__(self, name: str, exercises: list[str], extra_break_sec=0):
        # name of workout
        self.name = name
        self.exercises = exercises
        self.extra_break_sec = extra_break_sec


def encode_workout(o: Workout):
    # encode workout data as dict to export
    return {'name': o.name, 'exercises': o.exercises, 'extra_break_sec': o.extra_break_sec}


class WorkoutProcessor:
    # class handling workout signals in real time
    def __init__(self, exercise_processor: ExerciseProcessor, user):
        self.empty_workout = Workout('', [], 0)
        self.current_workout = self.empty_workout
        self.workout_break_exercise = Exercise('', 0, 0, 2, 0)
        self.workout_started = False
        self.workout_finished = False
        self.workout_break = False
        self.skip = False
        self.gui_select_next_exe = False
        self.exercise_pointer = 0
        self.exercise_processor = exercise_processor
        self.user = user

    def main(self):
        # main function to run current workout, to be called continuously
        # reset bits - they stay on only for one cycle
        self.workout_finished = False
        self.gui_select_next_exe = False
        # return if workout is not started
        if not self.workout_started:
            return
        # if exercise is finished or skipped load next
        if self.exercise_processor.exercise_finished or self.skip:
            self.skip = False
            # finish workout when there are no more exercises to load
            if self.exercise_pointer == len(self.current_workout.exercises):
                self.reset_workout()
                # set workout finished bit - it stays on only until next function call
                self.workout_finished = True
                return
            # If more exercises are present continue workout
            # Break between exercises
            if self.workout_break and self.current_workout.extra_break_sec > 0:
                self.workout_break = False
                self.exercise_processor.load_exercise(self.workout_break_exercise)
                self.exercise_processor.start_exercise()
            # Next exercise from the list
            elif self.load_next_exercise():
                self.workout_break = True
                self.exercise_processor.start_exercise()
                self.gui_select_next_exe = True

    def reset_workout(self):
        # reset current workout to start values
        self.workout_started = False
        self.workout_finished = False
        self.workout_break = False
        self.exercise_pointer = 0

    def load_next_exercise(self):
        # load next exercise from workout if available
        # return True if exercise is loaded, return False if no more exercises present in workout
        # or exercise not available
        if len(self.current_workout.exercises) > self.exercise_pointer:
            # get next exercise name
            next_exe_name = self.current_workout.exercises[self.exercise_pointer]
            # get exercise from user
            exercise = self.user.get_exercise(next_exe_name)
            if exercise is not None:
                # Load first exercise from current workout and start workout
                self.exercise_processor.load_exercise(exercise)
                self.exercise_pointer += 1
                return True
            return False

    def start_workout(self):
        # start current workout, return True if started successfully
        if not self.workout_started:
            self.exercise_processor.reset_exercise()
            # Load first exercise
            # return True if exercise was loaded
            if self.load_next_exercise():
                self.workout_started = True
                self.workout_break = True
                self.workout_break_exercise.breaktime_sec = self.current_workout.extra_break_sec
        return self.workout_started

    def load_workout(self, workout: Workout):
        # Load workout as current workout
        if not self.workout_started and workout is not None:
            self.current_workout = workout
            return True
        elif workout is None:
            self.current_workout = self.empty_workout
        return False

    def skip_exercise(self):
        # finish current exercise during the workout mode
        if self.workout_started:
            self.skip = True
            self.exercise_processor.reset_exercise()
