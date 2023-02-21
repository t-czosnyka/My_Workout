
class Exercise:

    def __init__(self, name='', worktime_sec =0, breaktime_sec=0, num_rounds=0, delay_sec=0):
        self.name = name
        self.worktime_sec = worktime_sec
        self.breaktime_sec = breaktime_sec
        self.num_rounds = num_rounds
        self.delay_sec = delay_sec

    def __str__(self):
        return self.name + f" :worktime:{self.worktime_sec}, breaktime:{self.breaktime_sec}, rounds:{self.num_rounds}, " \
                           f"delay:{self.delay_sec}"


def encode_exercise(o: Exercise):
    return {'name': o.name, 'worktime_sec': o.worktime_sec, 'breaktime_sec': o.breaktime_sec,
            'num_round': o.num_rounds, 'delay_sec': o.delay_sec}

