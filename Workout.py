class Workout:
    # class holding workout data with name and orderd list of exercises names
    def __init__(self, name: str, exercises: list[tuple], extra_break_sec=0):
        # name of workout
        self.name = name
        # exercises: list of tuples consisting of name and position in order
        self.exercises = exercises
        self.extra_break_sec = extra_break_sec


