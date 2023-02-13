from User import User
from tkinter import *
class Menu:

    def __init__(self, user: User, frame, pos_x: int, pos_y:int, curr_workout_list):
        self.user = user
        self.frame = frame
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.select_work_str = StringVar()
        self.curr_workout_list = curr_workout_list


    def create_workout_menu(self):
        # create option menu with workouts of current user
        if len(self.user.workouts) > 0:
            self.select_workout_menu = OptionMenu(self.frame, self.select_work_str, *self.user.workouts.keys(),
                                                  command=self.select_workout)
            # if no workouts selected, select first one
            if self.select_work_str.get() == '':
                key = list(self.user.workouts.keys())[0]
                self.select_work_str.set(key)
                self.select_workout(key)
        else:
            # if no workouts are available write empty value to menu options
            self.select_workout_menu = OptionMenu(self.frame, self.select_work_str, value='',
                                                  command=self.select_workout)
        self.select_workout_menu.place(x=self.pos_x, y=self.pos_y) #298, 394


    def select_workout(self, selected):
        # select workout from option menu and load it as current workout into list and user.curr_workout
        # when current workout is not started
        if not self.user.curr_workout_started:
            # if selected workout is found its content are written current workout list and user.curr_workout
            if self.user.load_workout(selected):
                size = self.curr_workout_list.size()
                self.curr_workout_list.delete(0, size)
                for i, exe in enumerate(self.user.workouts[selected].exercises, 1):
                    self.curr_workout_list.insert(i, exe[0])

    def disable(self):
        self.select_workout_menu.configure(state=DISABLED)

    def enable(self):
        self.select_workout_menu.configure(state=NORMAL)
