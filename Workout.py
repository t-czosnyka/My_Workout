class Workout:
    # class holding workout data with name and orderd list of exercises names
    def __init__(self, name, exercises: list[tuple]):
        # name of workout
        self.name = name
        # exercises: list of tuples consisting of name and position in order
        self.exercises = exercises
        self.exercise_finished = False
        self.started = False
        self.work_break = False

    def set_exe_finished(self):
        self.exercise_finished = True
        if self.work_break:
            self.work_break = False
        elif len(self.exercises) > 0:
            self.work_break = True

    def reset_exe_finished(self):
        self.exercise_finished = False

    def start_workout(self):
        self.started = True

    def finish_workout(self):
        self.reset_exe_finished()
        self.started = False

