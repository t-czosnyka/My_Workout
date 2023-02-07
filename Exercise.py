
class Exercise:

    def __init__(self,name='', worktime =0, breaktime=0, num_rounds=0, delay=0):
        self.name = name
        self.worktime = worktime
        self.breaktime = breaktime
        self.num_rounds = num_rounds
        self.delay = delay

    def __str__(self):
        return self.name + f" :worktime:{self.worktime}, breaktime:{self.breaktime}, rounds:{self.num_rounds}, delay:{self.delay}"



