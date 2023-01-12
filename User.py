

from Exercise import Exercise
class User:

    def __init__(self, name: str, email: str, password: str, admin: bool):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
        self.exercises = []
        self.workouts = []
        self.queue = []


    def run_exe(self, exe: Exercise):
        curr_round = 0
        curr_time = 0
        break_on = False
        if exe.num_rounds == 0 or exe.worktime == 0:
            return -1
        if exe.delay > 0:
            pass










