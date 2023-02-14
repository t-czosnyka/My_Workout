import copy

from User import User
from tkinter import *
from Exercise import Exercise
from tkinter import messagebox as mb
from DB import DB
from UserWindow import EditUserWindow
from WorkoutWindow import WorkoutWindow
from Menu import Menu


class Gui:

    def __init__(self, root, frame, user: User, DB):
        self.DB = DB
        self.root = root
        self.frame = frame
        self.frame.geometry('500x600')
        # when frame is closed - close hidden root
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.user = user

        # Timer Variables
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
        self.user_name_str = StringVar()
        self.exe_msg_str = StringVar()
        self.curr_exe_text_str = StringVar()

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
        self.user_name_str.set(f'{self.user.name}')


        ### User ###
        # Show user_name
        self.user_name_text = Label(self.frame, textvariable=self.user_name_str, font=("Helvetica", 10))
        self.user_name_text.place(x=10, y=10)

        # logout button
        self.logout_btn = Button(self.frame, text="Logout", command=self.log_out)
        self.logout_btn.place(x=10, y=35)

        # Delete user button
        self.delete_user_btn = Button(self.frame, text="Delete User", command=self.ask_delete_user, width=9)
        self.delete_user_btn.place(x=65, y=35)

        # Edit User Button
        self.edit_user_btn = Button(self.frame, text="Edit User", command=lambda : self.call_new_window(EditUserWindow), width=9)
        self.edit_user_btn.place(x=65, y=6)

        ### Timer ###
        # Create timer widgets
        self.mode_text = Label(self.frame, textvariable=self.curr_mode_str, font=("Helvetica", 40), fg=self.color_str.get())
        self.mode_text.grid(row=0, column=0, padx=(10, 0), columnspan=4)
        self.timer_text = Label(self.frame, textvariable=self.timer_value_str, font=("Helvetica", 80), fg=self.color_str.get())
        self.timer_text.grid(row=1, column=0, columnspan=3, padx=10)
        self.round_text = Label(self.frame, textvariable=self.round_num_int, font=("Helvetica", 40), fg=self.color_str.get())
        self.round_text.grid(row=1, column=4, padx=10)

        self.start_btn = Button(self.frame, text="Start", command=self.start_timer, width=20, height=2, state=DISABLED)
        self.start_btn.grid(row=2, column=0, columnspan=2)

        self.reset_btn = Button(self.frame, text="Reset", command=self.reset_exercise, width=20, height=2)
        self.reset_btn.grid(row=2, column=2, columnspan=2)

        ### Exercises ###
        # Create workout/exercise widgets

        self.exe_label = Label(self.frame, text="Exercise", font=("Helvetica", 20))
        self.exe_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.workout_label = Label(self.frame, text="Workout", font=("Helvetica", 20))
        self.workout_label.grid(row=3, column=2, columnspan=2, pady=(10, 0))

        self.exe_name_label = Label(self.frame, text="Exercise name:", font=("Helvetica", 10))
        self.exe_name_label.grid(row=4, column=0, sticky='w', padx=(20, 0))

        self.work_time_label = Label(self.frame, text="Work time:[min][sec]", font=("Helvetica", 10))
        self.work_time_label.grid(row=5, column=0, sticky='w', padx=(20, 0))

        self.break_time_label = Label(self.frame, text="Break time:[min][sec]", font=("Helvetica", 10))
        self.break_time_label.grid(row=6, column=0, sticky='w', padx=(20, 0))

        self.num_rounds_label = Label(self.frame, text="No. of rounds:", font=("Helvetica", 10))
        self.num_rounds_label.grid(row=7, column=0, sticky='w', padx=(20, 0))

        self.delay_time_label = Label(self.frame, text="Delay time:[sec]", font=("Helvetica", 10))
        self.delay_time_label.grid(row=8, column=0, sticky='w', padx=(20, 0))

        reg = self.frame.register(self.is_val_dig)
        reg2 = self.frame.register(self.is_val_str)

        self.exercise_name = Entry(self.frame, width=15, validate="key", validatecommand=(reg2, '%P'),
                                   textvariable=self.exercise_name_str)

        self.exercise_name.place(x=150, y=283)

        self.exercise_name_str.trace_add("write", self.exe_name)

        self.work_time_min = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                   textvariable=self.work_time_min_str)
        self.work_time_min.place(x=150, y=305)

        self.work_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                   textvariable=self.work_time_sec_str)
        self.work_time_sec.place(x=210, y=305)

        self.break_time_min = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.break_time_min_str)
        self.break_time_min.place(x=150, y=327)

        self.break_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.break_time_sec_str)
        self.break_time_sec.place(x=210, y=327)

        self.num_rounds = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5, textvariable=self.num_rounds_str)
        self.num_rounds.place(x=150, y=349)

        self.delay_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.delay_time_sec_str)
        self.delay_time_sec.place(x=150, y=371)

        # save exercise button
        self.save_btn = Button(self.frame, text="Save Exercise", command=self.save_exercise, state=DISABLED, width=12)
        self.save_btn.place(x=20, y=397)

        # delete exercise button
        self.delete_btn = Button(self.frame, text="Delete Exercise", command=self.delete_exercise, width=12)
        self.delete_btn.place(x=20,y=428)

        # status message label
        self.exe_msg = Label(self.frame, textvariable=self.exe_msg_str, wraplength=300)
        self.exe_msg.place(x=20,y=460)

        # create option menu based on user exercises
        self.create_exercise_menu()

        # Show current exercise:
        self.curr_exe_text = Label(self.frame,textvariable=self.curr_exe_text_str, font=("Helvetica", 20),
                                   fg=self.color_str.get())
        self.curr_exe_text.place(x=320, y=15)

        # trace changes in entry widgets
        self.work_time_min_str.trace_add("write", self.value_changed)
        self.work_time_sec_str.trace_add("write", self.value_changed)
        self.break_time_min_str.trace_add("write", self.value_changed)
        self.break_time_sec_str.trace_add("write", self.value_changed)
        self.num_rounds_str.trace_add("write", self.value_changed)
        self.delay_time_sec_str.trace_add("write", self.value_changed)

        ### Workouts #####
        # create workout start button
        self.start_work_btn = Button(self.frame, text='Start Workout', width=14, command=self.start_workout)
        self.start_work_btn.place(x=300, y=428)

        # create list with exercises in current workout
        self.curr_workout_exe_list = Listbox(self.frame, height=7, selectmode=SINGLE)
        self.curr_workout_exe_list.place(x=300, y=279)

        # create option menu with user workouts
        self.workout_menu = Menu(self.user, self.frame, 298, 395, self.curr_workout_exe_list)
        self.workout_menu.create_workout_menu()


        # Edit workout button
        self.edit_workout_btn = Button(self.frame, text="Edit Workout",
                                       command=lambda: self.call_new_window(WorkoutWindow), width=14)
        self.edit_workout_btn.place(x=300, y=458)



    def cont_update(self):
        # continuous update function
        # run exercise timer
        self.user.run_exe()
        # run workout
        self.user.run_workout()
        if self.user.curr_exe_finished:
            # single exercise finished
            if not self.user.curr_workout_started:
                self.user.reset_exe()
                self.pause_timer()
                self.user.update_display()
            # Exercise finished in workout mode
            else:
                # Reset and start next exercise
                self.select_exercise(self.user.curr_exe.name)
                self.user.reset_exe()
                if self.user.curr_workout_finished:
                    self.user.curr_workout_started = False
                    self.user.curr_workout_finished = False
                    self.pause_timer()
                    self.workout_menu.select_workout(self.user.curr_workout.name)
                else:
                    self.user.start_run()

        # update timer values and colors
        self.timer_value_str.set(self.user.my_timer.time_str)
        self.round_num_int.set(self.user.curr_exe_round)
        self.curr_mode_str.set(self.user.curr_exe_mode)
        if self.user.curr_exe.name != '':
            self.curr_exe_text_str.set(self.user.curr_exe.name)
        if self.user.curr_exe_mode == 'Delay' or self.user.curr_exe_mode == 'Break':
            self.mode_text.configure(fg="red")
            self.round_text.configure(fg="red")
            self.timer_text.configure(fg="red")
            self.curr_exe_text.configure(fg="red")
        else:
            self.mode_text.configure(fg="green")
            self.round_text.configure(fg="green")
            self.timer_text.configure(fg="green")
            self.curr_exe_text.configure(fg="green")

        # Disable/Enable widgets when workout is running
        if self.user.curr_workout_started:
            self.start_work_btn.configure(text="Workout Started",state=DISABLED)
            self.workout_menu.disable()
            self.select_exe_menu.configure(state=DISABLED)
            self.curr_workout_exe_list.configure(state=DISABLED)
        else:
            self.start_work_btn.configure(text="Start Workout",state=NORMAL)
            self.workout_menu.enable()
            self.select_exe_menu.configure(state=NORMAL)
            self.curr_workout_exe_list.configure(state=NORMAL)

        # recall again every 0.1s
        self.frame.after(100, self.cont_update)

    def start_timer(self):
        self.user.start_run()
        self.start_btn.configure(text="Pause", command=self.pause_timer)
        # Clear message
        self.exe_msg_str.set('')

    def start_workout(self):
        # start workout button function
        # if workout is loaded correctly start timer
        if self.user.start_workout():
            self.start_timer()
            # load current exercise from workout into entry widgets
            self.select_exercise(self.user.curr_exe.name)

    def pause_timer(self):
        self.user.stop_run()
        self.start_btn.configure(text="Start", command=self.start_timer)

    def reset_exercise(self):
        self.pause_timer()
        self.user.reset_exe()
        self.user.reset_workout()
        self.workout_menu.select_workout(self.user.curr_workout.name)
        self.update_curr_exercise()
        # Clear message
        self.exe_msg_str.set('')

    def get_str_var(self, str_var):
        # return int of stringvar or 0 if empty
        if str_var.get() != '':
            return int(str_var.get())
        else:
            return 0

    def get_exercise_inputs(self):
        # get inputs from exercise entry widgets
        name = self.exercise_name_str.get()
        work_time = self.get_str_var(self.work_time_min_str) * 60 + self.get_str_var(self.work_time_sec_str)
        break_time = self.get_str_var(self.break_time_min_str) * 60 + self.get_str_var(self.break_time_sec_str)
        num_rounds = self.get_str_var(self.num_rounds_str)
        delay = self.get_str_var(self.delay_time_sec_str)
        return [name, work_time, break_time, num_rounds, delay]

    def update_curr_exercise(self):
        # load values from entry widgets to current exercise or workout when exercise is not in progress
        if not self.user.curr_exe_started and not self.user.curr_exe_finished and not self.user.curr_workout_started:
            inputs = self.get_exercise_inputs()
            self.user.curr_exe.name = inputs[0]
            self.user.curr_exe.worktime_sec = inputs[1]
            self.user.curr_exe.breaktime_sec = inputs[2]
            self.user.curr_exe.num_rounds = inputs[3]
            self.user.curr_exe.delay_sec = inputs[4]
            self.user.check_exe()
            self.curr_exe_text_str.set(self.user.curr_exe.name)
            if self.user.curr_exe_valid:
                self.start_btn.configure(state=NORMAL)
            else:
                self.start_btn.configure(state=DISABLED)

    def value_changed(self, var, index, mode):
        # check values when entry widgest are changed
        self.update_curr_exercise()

    @staticmethod
    def is_val_dig(entry_input):  # validating function for entry widgets, max two digits allowed
        if (entry_input.isdigit() or entry_input == '') and len(entry_input) <= 2:
            return True
        else:
            return False

    @staticmethod
    def is_val_str(entry_input):  # validate exercise name - no more than 20 characters
        if len(entry_input) <= 20:
            return True
        else:
            return False

    def exe_name(self, var, index, mode):
        # possible to save exercise only if name is inserted
        if self.exercise_name_str.get() != '':
            self.save_btn.configure(state=NORMAL)
        else:
            self.save_btn.configure(state=DISABLED)

    def update_exercise_menu(self):
        # delete than recreate option menu
        self.select_exe_menu.destroy()
        self.create_exercise_menu()

    def create_exercise_menu(self):
        # create option menu with exercises of current user
        if len(self.user.exercises) > 0:
            self.select_exe_menu = OptionMenu(self.frame, self.select_exe_str, *self.user.exercises.keys(),
                                              command=self.select_exercise)
            # if no exercise selected, select first one
            if self.select_exe_str.get() == '':
                key = list(self.user.exercises.keys())[0]
                self.select_exe_str.set(key)
                self.select_exercise(key)
        else:
            # if no exercises are available write empty value to menu options
            self.select_exe_menu = OptionMenu(self.frame, self.select_exe_str, value='',
                                              command=self.select_exercise)
            self.select_exe_str.set('')
            self.exercise_name_str.set('')
        self.select_exe_menu.place(x=120, y=394)



    def select_exercise(self, selected):
        # insert selected values into entry widgets
        if selected in self.user.exercises:
            self.exercise_name_str.set(self.user.exercises[selected].name)
            self.work_time_min_str.set(str(self.user.exercises[selected].worktime_sec // 60))
            self.work_time_sec_str.set(str(self.user.exercises[selected].worktime_sec % 60))
            self.break_time_min_str.set(str(self.user.exercises[selected].breaktime_sec // 60))
            self.break_time_sec_str.set(str(self.user.exercises[selected].breaktime_sec % 60))
            self.num_rounds_str.set(str(self.user.exercises[selected].num_rounds))
            self.delay_time_sec_str.set(str(self.user.exercises[selected].delay_sec))


    def log_out(self):
        # logout by unhide main window, close frame
        self.frame.destroy()
        self.root.deiconify()

    def on_closing(self):
        # close root if frame is closed
        self.root.destroy()

    def save_exercise(self):
        # save button function
        # save entry widget values into Exercise object and database
        if self.user.curr_workout_started:
            mb.showerror('Error', 'Workout in progress.')
            return
        inputs = self.get_exercise_inputs()
        # Save data to DB, in case of error return
        res, error = self.DB.save_exercise(self.user.name, *inputs)
        if not res:
            # Display message
            mb.showerror("Database Error.", error)
            return
        # Create or update Exercise object if DB operation was susccesful
        self.user.save_exercise(inputs)
        # Update options in menu and select saved exercise
        self.update_exercise_menu()
        self.select_exe_str.set(inputs[0])
        # Display message
        self.exe_msg_str.set('Exercise saved.')

    def delete_exercise(self):
        # delete currently selected exercise from user class and DB
        # cannot change exercises when workout in progress
        if self.user.curr_workout_started:
            mb.showerror('Error', 'Workout in progress.')
            return

        # exercise name from entry widget:
        exe_name = self.exercise_name_str.get()
        # delete from DB
        res, error = self.DB.delete_exercise(self.user.name, exe_name)
        # check if successfully deleted from DB
        if not res:
            # Display message
            mb.showerror("Database Error.", error)
            return
        # delete current name from select menu
        self.select_exe_str.set('')
        # delete current name form user exercises
        self.user.delete_exercise(exe_name)
        self.update_exercise_menu()
        # update currently selected workout exercises list
        self.workout_menu.select_workout(self.workout_menu.select_work_str.get())
        # Display message
        self.exe_msg_str.set('Exercise deleted.')

    def ask_delete_user(self):
        res = mb.askquestion('Delete User', 'Do you really want to delete user')
        if res == 'yes':
            self.delete_user()
        else:
            return

    def delete_user(self):
        user_name = self.user.name
        res, error = self.DB.delete_user(user_name)
        if not res:
            mb.showinfo('Return', 'Operation failed.')
            return
        self.log_out()
        mb.showinfo('OK', 'User deleted.')

    def call_new_window(self, WindowClass):
        # Hide Gui and call new window
        self.frame.withdraw()
        window = Toplevel()
        WindowClass(self.frame, window, self.DB, self.user)


