from User import User
from tkinter import *
class Menu:
    # class creates select workout menu based on user workouts, writes selected workout data into widgets
    def __init__(self, user: User, frame, pos_x: int, pos_y:int, curr_workout_list, disable_break_entry: bool):
        self.user = user
        self.frame = frame
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.curr_workout_list = curr_workout_list

        # Define variables
        self.select_work_str = StringVar()
        self.workout_break_sec_str = StringVar()
        # Initialize variables
        self.workout_break_sec_str.set('0')

        # Create widgets
        self.workout_break_sec_label = Label(self.frame, text="Extra break[sec]:")
        self.workout_break_sec_label.place(x=pos_x, y=pos_y)

        # validating function for extra break time input
        val = self.frame.register(lambda x: self.user.validate_time_input(x, 3))

        self.workout_break_sec = Entry(self.frame, textvariable=self.workout_break_sec_str, width=4, validate='key',
                                       validatecommand=(val, '%P'))

        self.workout_break_sec.place(x=pos_x + 95, y=pos_y)
        if disable_break_entry:
            self.workout_break_sec.configure(state=DISABLED)
        self.create_menu()


    def create_menu(self):
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
            self.curr_workout_list.delete(0, END)
            self.select_work_str.set('')


        self.select_workout_menu.configure(width=11)
        self.select_workout_menu.place(x=self.pos_x, y=self.pos_y + 25)

    def update_menu(self):
        # destroy and create new menu
        self.select_workout_menu.destroy()
        self.create_menu()
        self.refresh_workout()


    def select_workout(self, selected):
        # select workout from option menu and load it as current workout into list and user.curr_workout
        # when current workout is not started
        if not self.user.curr_workout_started:
            self.select_work_str.set(selected)
            # if selected workout is found its content are written current workout list and user.curr_workout
            if self.user.load_workout(selected):
                self.curr_workout_list.delete(0, END)
                # write workout break into variable
                self.workout_break_sec_str.set(str(self.user.curr_workout.extra_break_sec))
                if len(self.user.workouts) == 0:
                    return
                for i, exe in enumerate(self.user.workouts[selected].exercises, 1):
                    self.curr_workout_list.insert(i, exe[0])


    def refresh_workout(self):
        # re-select currently selected workout to apply changes
        self.select_workout(self.select_work_str.get())

    def disable(self):
        self.select_workout_menu.configure(state=DISABLED)

    def enable(self):
        self.select_workout_menu.configure(state=NORMAL)
