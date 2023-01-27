from User import User
from tkinter import *
from Exercise import Exercise
from Login import Login
from DB import DB



class Gui:

    def __init__(self, root, user: User, DB):
        self.DB =DB
        self.root = root
        self.root.geometry('500x600')
        self.user = user

        #Timer Variables
        self.curr_mode_str = StringVar()
        self.timer_value_str = StringVar()
        self.round_num_int = IntVar()
        self.color_str = StringVar()

        # Entry widget variables:
        self.work_time_min_str = StringVar()
        self.work_time_sec_str = StringVar()

        self.break_time_min_str = StringVar()
        self.break_time_sec_str = StringVar()

        self.num_rounds_str = StringVar()
        self.exercise_name_str = StringVar()

        self.delay_time_sec_str = StringVar()
        self.select_exe_str = StringVar()

        # Initialize tkinter variables
        self.timer_value_str.set("00:00:00")
        self.round_num_int.set(0)
        self.curr_mode_str.set("Ready")
        self.color_str.set("Green")

        self.work_time_min_str.set('0')
        self.work_time_sec_str.set('0')

        self.break_time_min_str.set('0')
        self.break_time_sec_str.set('0')

        self.num_rounds_str.set('0')

        self.delay_time_sec_str.set('0')

        self.select_exe_str.set('')

        # Create timer widgets
        self.mode_text = Label(root, textvariable=self.curr_mode_str, font=("Helvetica", 40), fg=self.color_str.get())
        self.mode_text.grid(row=0, column=0, padx=(10, 0), columnspan=4)
        self.timer_text = Label(root, textvariable=self.timer_value_str, font=("Helvetica", 80), fg=self.color_str.get())
        self.timer_text.grid(row=1, column=0, columnspan=3, padx=10)
        self.round_text = Label(root, textvariable=self.round_num_int, font=("Helvetica", 40), fg=self.color_str.get())
        self.round_text.grid(row=1, column=4, padx=10)

        self.start_btn = Button(root, text="Start", command=self.start_timer, width=20, height=2, state=DISABLED)
        self.start_btn.grid(row=2, column=0, columnspan=2)

        self.reset_btn = Button(root, text="Reset", command=self.reset_exercise, width=20, height=2)
        self.reset_btn.grid(row=2, column=2, columnspan=2)

        #Create workout/exercise widgets

        self.exe_label = Label(root, text="Exercise", font=("Helvetica", 20))
        self.exe_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.workout_label = Label(root, text="Workout", font=("Helvetica", 20))
        self.workout_label.grid(row=3, column=2, columnspan=2, pady=(10, 0))

        self.exe_name_label = Label(root, text="Exercise name:", font=("Helvetica", 10))
        self.exe_name_label.grid(row=4, column=0, sticky='w', padx=(20, 0))

        self.work_time_label = Label(root, text="Work time:[min][sec]", font=("Helvetica", 10))
        self.work_time_label.grid(row=5, column=0, sticky='w', padx=(20, 0))

        self.break_time_label = Label(root, text="Break time:[min][sec]", font=("Helvetica", 10))
        self.break_time_label.grid(row=6, column=0, sticky='w', padx=(20, 0))

        self.num_rounds_label = Label(root, text="No. of rounds:", font=("Helvetica", 10))
        self.num_rounds_label.grid(row=7, column=0, sticky='w', padx=(20, 0))

        self.delay_time_label = Label(root, text="Delay time:[sec]", font=("Helvetica", 10))
        self.delay_time_label.grid(row=8, column=0, sticky='w', padx=(20, 0))

        reg = root.register(self.is_val_dig)
        reg2 = root.register(self.is_val_str)

        self.exercise_name = Entry(root, width=15, validate="key", validatecommand=(reg2, '%P'),
                                    textvariable=self.exercise_name_str)

        self.exercise_name.place(x=150, y=283)

        self.exercise_name_str.trace_add("write", self.exe_name)

        self.work_time_min = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,
                              textvariable=self.work_time_min_str)
        self.work_time_min.place(x=150, y=305)

        self.work_time_sec = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,
                              textvariable=self.work_time_sec_str)
        self.work_time_sec.place(x=210, y=305)

        self.break_time_min = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,
                               textvariable=self.break_time_min_str)
        self.break_time_min.place(x=150, y=327)

        self.break_time_sec = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,
                               textvariable=self.break_time_sec_str)
        self.break_time_sec.place(x=210, y=327)

        self.num_rounds = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5, textvariable=self.num_rounds_str)
        self.num_rounds.place(x=150, y=349)

        self.delay_time_sec = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,
                               textvariable=self.delay_time_sec_str)
        self.delay_time_sec.place(x=150, y=371)

        # trace changes in entry widgets
        self.work_time_min_str.trace_add("write", self.value_changed)
        self.work_time_sec_str.trace_add("write", self.value_changed)
        self.break_time_min_str.trace_add("write", self.value_changed)
        self.break_time_sec_str.trace_add("write", self.value_changed)
        self.num_rounds_str.trace_add("write", self.value_changed)
        self.delay_time_sec_str.trace_add("write", self.value_changed)

        # save button
        self.save_btn = Button(root, text="Save Exercise", command=self.save_exercise, state=DISABLED)
        self.save_btn.place(x=20, y=394)

        # select previously saved exercise from drop down menu
        self.select_exe_menu = OptionMenu(root, self.select_exe_str, *self.user.exercises.keys(), command=self.select_exe)
        self.select_exe_menu.place(x=120, y=392)

        #logout button
        self.logout_btn = Button(self.root, text="Logout", command=self.log_out)
        self.logout_btn.place(x=120, y=420)

    def start_timer(self):
        self.user.running = True
        self.start_btn.configure(text="Pause", command=self.pause_timer)

    def pause_timer(self):
        self.user.running = False
        self.start_btn.configure(text="Start", command=self.start_timer)

    def reset_exercise(self):
        self.pause_timer()
        self.user.reset_exe()
        self.load_exercise()

    def get_str_var(self, str_var):
        # return int of stringvar or 0 if empty
        if str_var.get() != '':
            return int(str_var.get())
        else:
            return 0

    def get_inputs(self):
        # get inputs from exercise entry widgets
        work_time = self.get_str_var(self.work_time_min_str) * 60 + self.get_str_var(self.work_time_sec_str)
        break_time = self.get_str_var(self.break_time_min_str) * 60 + self.get_str_var(self.break_time_sec_str)
        num_rounds = self.get_str_var(self.num_rounds_str)
        delay = self.get_str_var(self.delay_time_sec_str)
        return [work_time, break_time, num_rounds, delay]

    def load_exercise(self):
        # load values from entry widgets to current exercise
        if not self.user.curr_exe.started and not self.user.curr_exe.finished:
            inputs = self.get_inputs()
            self.user.curr_exe.worktime = inputs[0]
            self.user.curr_exe.breaktime = inputs[1]
            self.user.curr_exe.num_rounds = inputs[2]
            self.user.curr_exe.delay = inputs[3]
            self.user.check_exe()
            if self.user.valid_exe:
                self.start_btn.configure(state=NORMAL)
            else:
                self.start_btn.configure(state=DISABLED)

    def value_changed(self, var, index, mode):
        # check values when entry widgest are changed
        self.load_exercise()

    def save_exercise(self):
        # save button function
        # save entry widget values into Exercise object
        name = self.exercise_name_str.get()
        inputs = self.get_inputs()
        if name in self.user.exercises:
            self.user.exercises[name].worktime = inputs[0]
            self.user.exercises[name].breaktime = inputs[1]
            self.user.exercises[name].num_rounds = inputs[2]
            self.user.exercises[name].delay = inputs[3]
        else:
            self.user.exercises[name] = Exercise(name, *inputs)
        self.update_option_menu()

    def is_val_dig(self, input):  # validating function for entry widgets, max two digits allowed
        if (input.isdigit() or input == '') and len(input) <= 2:
            return True
        else:
            return False

    def is_val_str(self, input):  # validate exercise name - no more than 20 characters
        if len(input) <= 20:
            return True
        else:
            return False

    def exe_name(self, var, index, mode):
        # possible to save exercise only if name is inserted
        if self.exercise_name_str.get() != '':
            self.save_btn.configure(state=NORMAL)
        else:
            self.save_btn.configure(state=DISABLED)

    def update_option_menu(self):

        # after adding new exercise recreate OptionMenu widget with new options
        self.select_exe_menu.destroy()
        self.select_exe_menu = OptionMenu(self.root, self.select_exe_str, *self.user.exercises.keys(),
                                          command=self.select_exe)
        self.select_exe_menu.place(x=120, y=392)

    def select_exe(self,selected):
        # insert selected values into entry widgets
        if selected in self.user.exercises:
            self.exercise_name_str.set(self.user.exercises[selected].name)
            self.work_time_min_str.set(str(self.user.exercises[selected].worktime // 60))
            self.work_time_sec_str.set(str(self.user.exercises[selected].worktime % 60))
            self.break_time_min_str.set(str(self.user.exercises[selected].breaktime // 60))
            self.break_time_sec_str.set(str(self.user.exercises[selected].breaktime % 60))
            self.num_rounds_str.set(str(self.user.exercises[selected].num_rounds))
            self.delay_time_sec_str.set(str(self.user.exercises[selected].delay))

    def update(self):
        #continous update function
        self.user.run_exe()
        if self.user.curr_exe.finished:
            self.pause_timer()
            self.user.reset_exe()

        self.timer_value_str.set(self.user.my_timer.time_str)
        self.round_num_int.set(self.user.curr_round)
        self.curr_mode_str.set(self.user.mode)
        if self.user.mode == 'Delay' or self.user.mode == 'Break':
            self.mode_text.configure(fg="red")
            self.round_text.configure(fg="red")
            self.timer_text.configure(fg="red")
        else:
            self.mode_text.configure(fg="green")
            self.round_text.configure(fg="green")
            self.timer_text.configure(fg="green")
        self.root.after(100, self.update)

    def log_out(self):
        #logout by hiding main window, calling login window top
        self.root.withdraw()
        top = Toplevel()
        Login(top, self.root, self.DB)






