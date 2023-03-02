import json
from User import User
from tkinter import *
from tkinter import filedialog, messagebox as mb
from UserWindow import EditUserWindow
from EditWorkoutWindow import EditWorkoutWindow
from WorkoutMenu import WorkoutMenu
from winsound import *
from Exercise import Exercise, ExerciseProcessor
from Workout import WorkoutProcessor


class Gui:

    def __init__(self, root, frame, user: User, DB, exercise_processor: ExerciseProcessor,
                 workout_processor: WorkoutProcessor):
        self.DB = DB
        self.root = root
        self.frame = frame
        self.frame.geometry('500x550')
        # disable resizing
        self.frame.resizable(False, False)
        # when frame is closed - close hidden root
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.user = user
        self.exercise_processor = exercise_processor
        self.workout_processor = workout_processor

        # Timer Variables
        self.curr_mode_str = StringVar()
        self.timer_value_str = StringVar()
        self.round_num_int = IntVar()
        self.color_str = StringVar()
        self.total_time_passed_str = StringVar()
        self.work_time_passed_str = StringVar()
        self.break_time_passed_str = StringVar()

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
        self.current_exercise_text_str = StringVar()
        self.workout_extra_break_sec_str = StringVar()

        # Initialize tkinter variables
        self.timer_value_str.set("00:00:00")
        self.total_time_passed_str.set("00:00:00")
        self.work_time_passed_str.set("00:00:00")
        self.break_time_passed_str.set("00:00:00")
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
        self.workout_extra_break_sec_str.set('0')

        ### User ###
        # Show user_name
        self.user_name_text = Label(self.frame, textvariable=self.user_name_str, font=("Helvetica", 10),
                                    relief="sunken", width=12, anchor=W)
        self.user_name_text.place(x=10, y=20)

        # Create Menu bar for user options
        # create a menubar
        self.menubar = Menu(self.frame)
        self.frame.config(menu=self.menubar)
        # create a menu
        self.user_menu = Menu(self.menubar, tearoff=0)
        self.help_menu = Menu(self.menubar, tearoff=0)

        # add a menu item to the menu
        self.user_menu.add_command(label='Logout', command=self.log_out)
        self.user_menu.add_command(label='Edit User', command=self.call_edit_user_window)
        self.user_menu.add_command(label='Delete User', command=self.ask_delete_user)
        self.user_menu.add_command(label='Import config', command=self.import_config)
        self.user_menu.add_command(label='Export config', command=self.export_config)
        self.user_menu.add_command(label='Exit', command=self.root.destroy)

        self.help_menu.add_command(label='Help', command=self.show_help)

        # add the File menu to the menubar
        self.menubar.add_cascade(label="User", menu=self.user_menu)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        ### Timer ###
        # Create timer widgets
        self.mode_text = Label(self.frame, textvariable=self.curr_mode_str, font=("Helvetica", 30),
                               fg=self.color_str.get())
        self.mode_text.grid(row=0, column=0, padx=(10, 0), columnspan=4)
        self.timer_text = Label(self.frame, textvariable=self.timer_value_str, font=("Helvetica", 80),
                                fg=self.color_str.get())
        self.timer_text.grid(row=1, column=0, columnspan=3, padx=8)
        self.round_text = Label(self.frame, textvariable=self.round_num_int, font=("Helvetica", 35),
                                fg=self.color_str.get())
        self.round_text.grid(row=1, column=4, padx=0)

        self.start_btn = Button(self.frame, text="Start", command=self.start_exercise, width=20, height=2,
                                state=DISABLED)
        self.start_btn.grid(row=2, column=0, columnspan=2)

        self.reset_btn = Button(self.frame, text="Reset", command=self.reset_exercise, width=20, height=2)
        self.reset_btn.grid(row=2, column=2, columnspan=2)

        # time passed
        self.total_time_passed_label = Label(self.frame, text="Total time:", font=("Helvetica", 12))
        self.total_time_passed_label.place(x=20, y=460)
        self.total_time_passed = Label(self.frame, textvariable=self.total_time_passed_str, font=("Helvetica", 15))
        self.total_time_passed.place(x=170, y=457)

        self.work_time_passed_label = Label(self.frame, text="Total work time:", font=("Helvetica", 12))
        self.work_time_passed_label.place(x=20, y=485)
        self.work_time_passed = Label(self.frame, textvariable=self.work_time_passed_str, font=("Helvetica", 15))
        self.work_time_passed.place(x=170, y=482)

        self.break_time_passed_label = Label(self.frame, text="Total break time:", font=("Helvetica", 12))
        self.break_time_passed_label.place(x=20, y=510)
        self.break_time_passed = Label(self.frame, textvariable=self.break_time_passed_str, font=("Helvetica", 15))
        self.break_time_passed.place(x=170, y=507)

        ### Exercises ###
        # Create exercise widgets

        self.exe_label = Label(self.frame, text="Exercise", font=("Helvetica", 20))
        self.exe_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        self.workout_label = Label(self.frame, text="Workout", font=("Helvetica", 20))
        self.workout_label.grid(row=3, column=2, columnspan=2, pady=(10, 0))

        self.exe_name_label = Label(self.frame, text="Exercise name:", font=("Helvetica", 10))
        self.exe_name_label.place(x=20, y=278)

        self.work_time_label = Label(self.frame, text="Work time[min][sec]:", font=("Helvetica", 10))
        self.work_time_label.place(x=20, y=300)

        self.break_time_label = Label(self.frame, text="Break time[min][sec]:", font=("Helvetica", 10))
        self.break_time_label.place(x=20, y=322)

        self.num_rounds_label = Label(self.frame, text="No. of rounds:", font=("Helvetica", 10))
        self.num_rounds_label.place(x=20, y=344)

        self.delay_time_label = Label(self.frame, text="Delay time[sec]:", font=("Helvetica", 10))
        self.delay_time_label.place(x=20, y=366)

        # validating functions for exercise entry widgets
        reg = self.frame.register(lambda x: self.user.validate_time_input(x, 2))
        reg2 = self.frame.register(self.user.validate_name_input)

        self.exercise_name = Entry(self.frame, width=15, validate="key", validatecommand=(reg2, '%P'),
                                   textvariable=self.exercise_name_str)

        self.exercise_name.place(x=150, y=280)

        self.work_time_min = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                   textvariable=self.work_time_min_str)
        self.work_time_min.place(x=150, y=301)

        self.work_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                   textvariable=self.work_time_sec_str)
        self.work_time_sec.place(x=210, y=301)

        self.break_time_min = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.break_time_min_str)
        self.break_time_min.place(x=150, y=323)

        self.break_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.break_time_sec_str)
        self.break_time_sec.place(x=210, y=323)

        self.num_rounds = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                textvariable=self.num_rounds_str)
        self.num_rounds.place(x=150, y=345)

        self.delay_time_sec = Entry(self.frame, validate="key", validatecommand=(reg, '%P'), width=5,
                                    textvariable=self.delay_time_sec_str)
        self.delay_time_sec.place(x=150, y=367)

        # save exercise button
        self.save_exercise_btn = Button(self.frame, text="Save Exercise", command=self.save_exercise, state=DISABLED,
                                        width=12)
        self.save_exercise_btn.place(x=20, y=397)

        # delete exercise button
        self.delete_btn = Button(self.frame, text="Delete Exercise", command=self.delete_exercise, width=12)
        self.delete_btn.place(x=20, y=427)

        # create option menu based on user exercises
        self.create_exercise_menu()

        # Show current exercise:
        self.curr_exe_text = Label(self.frame, textvariable=self.current_exercise_text_str, font=("Helvetica", 20),
                                   fg=self.color_str.get(), width=10, anchor=W)
        self.curr_exe_text.place(x=320, y=15)

        # trace changes in exercise entry widgets
        self.work_time_min_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.work_time_sec_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.break_time_min_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.break_time_sec_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.num_rounds_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.delay_time_sec_str.trace_add("write", self.load_widget_values_to_current_exercise)
        self.exercise_name_str.trace_add("write", self.load_widget_values_to_current_exercise)

        ### Workouts #####
        # Create workout widgets
        # create list with exercises in current workout
        self.curr_workout_exe_list = Listbox(self.frame, height=7, selectmode=SINGLE)
        self.curr_workout_exe_list.place(x=300, y=279)

        # create option menu with user workouts
        self.workout_menu = WorkoutMenu(self.user, self.frame, 298, 400, self.curr_workout_exe_list, True,
                                        self.workout_processor)

        # create workout start button
        self.start_work_btn = Button(self.frame, text='Start Workout', width=14, command=self.start_workout)
        self.start_work_btn.place(x=300, y=458)

        # Edit workout button
        self.edit_workout_btn = Button(self.frame, text="Edit Workout",
                                       command=self.call_edit_workout_window, width=14)
        self.edit_workout_btn.place(x=300, y=488)

        # Skip exercise button, finish current exercise in workout
        self.skip_exercise_btn = Button(self.frame, text="Skip Exercise",
                                        command=self.skip_exercise, width=14, state=DISABLED)
        self.skip_exercise_btn.place(x=300, y=518)

        # Call continuous update function
        self.continuous_update()

    def continuous_update(self):
        # continuous update function runs every 0.1s - call main processor function, updates gui
        # run main processor functions to control workouts and exercises
        self.exercise_processor.main()
        self.workout_processor.main()

        # next exercise request -> load current exercise data into widgets
        if self.workout_processor.gui_select_next_exe:
            self.select_exercise(self.exercise_processor.current_exercise.name)

        # update timer values and colors
        self.timer_value_str.set(self.exercise_processor.my_timer.active_time_str)
        self.total_time_passed_str.set(self.exercise_processor.my_timer.total_time_passed_str)
        self.work_time_passed_str.set(self.exercise_processor.my_timer.work_time_passed_str)
        self.break_time_passed_str.set(self.exercise_processor.my_timer.break_time_passed_str)
        self.round_num_int.set(self.exercise_processor.current_round)
        self.curr_mode_str.set(self.exercise_processor.current_exercise_mode)

        # single exercise is finished -> adjust widgets, show message and reset request
        if self.exercise_processor.exercise_finished and not self.workout_processor.workout_started:
            self.pause_exercise()

        # workout is finished -> adjust widgets, show message and reset request
        if self.workout_processor.workout_finished:
            self.pause_exercise()
            self.adjust_workout_widgets_not_started()
            mb.showinfo("Info", "Workout finished.")

        if self.exercise_processor.current_exercise_mode == 'Delay' or\
                self.exercise_processor.current_exercise_mode == 'Break':
            self.mode_text.configure(fg="red")
            self.round_text.configure(fg="red")
            self.timer_text.configure(fg="red")
            self.curr_exe_text.configure(fg="red")
        else:
            self.mode_text.configure(fg="green")
            self.round_text.configure(fg="green")
            self.timer_text.configure(fg="green")
            self.curr_exe_text.configure(fg="green")

        # refresh workout list after changes
        if self.user.req_workout_update:
            self.workout_menu.select_work_str.set('')
            self.workout_menu.update_menu()
            self.user.req_workout_update_reset()

        # play sound if requested by exercise processor
        if self.exercise_processor.req_play_sound:
            PlaySound('bell.wav', SND_FILENAME | SND_ASYNC)

        # possible to start only if inputs are valid
        if self.exercise_processor.current_exercise_valid:
            self.start_btn.configure(state=NORMAL)
        else:
            self.start_btn.configure(state=DISABLED)

        # possible to save exercise only if name is inserted
        if self.exercise_name_str.get() != '':
            self.save_exercise_btn.configure(state=NORMAL)
        else:
            self.save_exercise_btn.configure(state=DISABLED)

        self.current_exercise_text_str.set(self.exercise_processor.current_exercise.name)
        # recall again every 0.1s
        self.frame.after(100, self.continuous_update)

    def start_exercise(self):
        # start current exercise, change start button to pause button
        self.exercise_processor.start_exercise()
        self.start_btn.configure(text="Pause", command=self.pause_exercise)

    def pause_exercise(self):
        # pause current exercise, change pause button to start button
        self.exercise_processor.pause_exercise()
        self.start_btn.configure(text="Start", command=self.start_exercise)

    def reset_exercise(self):
        # pause and reset current exercise
        self.pause_exercise()
        self.exercise_processor.reset_exercise()
        self.load_widget_values_to_current_exercise()
        # self.workout_processor.reset_workout()
        # # reload workout
        # self.load_widget_values_to_current_exercise()
        # # enable workout widgets
        # self.adjust_workout_widgets_started()

    def start_workout(self):
        # start workout button function
        # if workout is loaded correctly start timer
        if self.workout_processor.start_workout():
            self.start_exercise()
            # load current exercise from workout into entry widgets
            self.select_exercise(self.exercise_processor.current_exercise.name)
            # updated workout start button and disable workout widgets
            self.adjust_workout_widgets_started()

    def reset_workout(self):
        # stop and reset current workout
        self.pause_exercise()
        self.exercise_processor.reset_exercise()
        self.workout_processor.reset_workout()
        # enable workout widgets
        self.adjust_workout_widgets_not_started()

    def get_exercise_inputs(self):
        # get inputs from exercise entry widgets
        name = self.exercise_name_str.get()
        work_time = self.user.get_str_var(self.work_time_min_str) * 60 + self.user.get_str_var(self.work_time_sec_str)
        break_time = self.user.get_str_var(self.break_time_min_str) * 60 + self.user.get_str_var(self.break_time_sec_str)
        num_rounds = self.user.get_str_var(self.num_rounds_str)
        delay = self.user.get_str_var(self.delay_time_sec_str)
        return [name, work_time, break_time, num_rounds, delay]

    def load_widget_values_to_current_exercise(self, *args):
        # load values from entry widgets to current exercise
        if not self.workout_processor.workout_started:
            self.exercise_processor.load_exercise(Exercise(*self.get_exercise_inputs()))

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
        self.select_exe_menu.place(x=145, y=394)
        self.select_exe_menu.configure(width=10, anchor=W)

    def select_exercise(self, selected):
        # insert selected values into entry widgets
        if selected in self.user.exercises:
            self.select_exe_str.set(selected)
            self.exercise_name_str.set(self.user.exercises[selected].name)
            self.work_time_min_str.set(str(self.user.exercises[selected].worktime_sec // 60))
            self.work_time_sec_str.set(str(self.user.exercises[selected].worktime_sec % 60))
            self.break_time_min_str.set(str(self.user.exercises[selected].breaktime_sec // 60))
            self.break_time_sec_str.set(str(self.user.exercises[selected].breaktime_sec % 60))
            self.num_rounds_str.set(str(self.user.exercises[selected].num_rounds))
            self.delay_time_sec_str.set(str(self.user.exercises[selected].delay_sec))
            self.load_widget_values_to_current_exercise()

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
        if self.workout_processor.workout_started:
            mb.showerror('Error', 'Workout in progress.')
            return
        inputs = self.get_exercise_inputs()
        # Save data to DB, in case of error return
        res, error = self.DB.save_exercise(self.user.name, *inputs)
        if not res:
            # Display message
            mb.showerror("Database Error.", error)
            return
        # Create or update Exercise object if DB operation was successful
        self.user.save_exercise(inputs)
        # Update options in menu and select saved exercise
        self.update_exercise_menu()
        self.select_exe_str.set(inputs[0])
        # Display message
        mb.showinfo('Success', 'Exercise saved.')

    def delete_exercise(self):
        # delete currently selected exercise from user class and DB
        # cannot change exercises when workout in progress
        if self.workout_processor.workout_started:
            mb.showerror('Error', 'Workout in progress.')
            return

        # exercise name from entry widget:
        exe_name = self.exercise_name_str.get()
        if exe_name == '':
            mb.showerror("Error.", "Exercise name cannot be empty.")
            return
        # delete from DB
        res, error = self.DB.delete_exercise(self.user.name, exe_name)
        # check if deleted correctly -> return if not deleted
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
        mb.showinfo('Success', 'Exercise deleted.')

    def ask_delete_user(self):
        res = mb.askquestion('Delete User', 'Do you really want to delete user')
        if res == 'yes':
            self.delete_user()
        else:
            return

    def delete_user(self):
        user_name = self.user.name
        result, error = self.DB.delete_user(user_name)
        if not result:
            mb.showerror('Database error.', error)
            return
        self.log_out()
        mb.showinfo('OK', 'User deleted.')

    def call_edit_user_window(self):
        # Hide Gui and call edit user window
        self.frame.withdraw()
        window = Toplevel()
        EditUserWindow(self.frame, window, self.DB, self.user)

    def call_edit_workout_window(self):
        # Hide Gui and call edit workout window
        self.frame.withdraw()
        window = Toplevel()
        EditWorkoutWindow(self.frame, window, self.DB, self.user, self.workout_menu.select_work_str.get(),
                          self.workout_processor)

    def adjust_workout_widgets_not_started(self):
        # adjust workout widgets when workout is not started
        self.start_work_btn.configure(text="Start Workout", state=NORMAL, command=self.start_workout)
        self.workout_menu.enable()
        self.select_exe_menu.configure(state=NORMAL)
        self.curr_workout_exe_list.configure(state=NORMAL)
        self.edit_workout_btn.configure(state=NORMAL)
        self.skip_exercise_btn.configure(state=DISABLED)

    def adjust_workout_widgets_started(self):
        # adjust workout widgets when workout started
        self.start_work_btn.configure(text="Reset Workout", state=NORMAL, command=self.reset_workout)
        self.workout_menu.disable()
        self.select_exe_menu.configure(state=DISABLED)
        self.curr_workout_exe_list.configure(state=DISABLED)
        self.edit_workout_btn.configure(state=DISABLED)
        self.skip_exercise_btn.configure(state=NORMAL)

    def skip_exercise(self):
        # finish current exercise during workout
        self.start_exercise()
        self.workout_processor.skip_exercise()

    def import_config(self):
        # import JSON file with User exercises and workouts
        # get file location from dialog window
        location = filedialog.askopenfilename(initialdir="/", title="Choose file to import",
                                                         filetypes=(("JSON files", "*.json"),))
        # return if location is empty
        if location == "":
            return
        # read from file
        try:
            with open(location, mode="r") as f:
                data = json.load(f)
        except FileNotFoundError:
            mb.showerror("Error.", "File not found.")
            return
        except json.decoder.JSONDecodeError as e:
            mb.showerror("Error.", "Cant read JSON file. "+e.msg)
            return

        # save data from file into DB and user data
        try:
            # save imported exercises to user and database
            for exe in data[0]['exercises']:
                values = list(exe.values())
                self.user.save_exercise(values)
                self.DB.save_exercise(self.user.name, *values)
            # save imported workouts to user and database
            for work in data[1]['workouts']:
                values = list(work.values())
                exercises = values[1]
                # check if exercises from file are available
                for exercise in exercises:
                    if exercise not in self.user.exercises:
                        # raise custom exception
                        raise ExerciseNotExists(f"Exercise {exercise} does not exist.")
                self.user.save_workout(*values)
                self.DB.save_workout(self.user.name, *values)
        except ExerciseNotExists as e:
            mb.showerror("Error", e.message)
        except KeyError as e:
            mb.showerror("Error", "Wrong data format. " + str(e))
        else:
            mb.showinfo("Info", "Data import successful.")
        # update exercise and workout menu
        self.update_exercise_menu()
        self.workout_menu.update_menu()

    def export_config(self):
        # export user exercises and workouts to JSON file
        location = filedialog.asksaveasfilename(initialdir="/", title="Choose location to export",
                                                filetypes=(("JSON files", "*.json"),))
        exe_data = self.user.encode_exercises()
        workout_data = self.user.encode_workouts()

        # return if location is empty
        if location == "":
            return
        if not location.__contains__('.json'):
            location = location+'.json'

        with open(location, mode="w") as f:
            json.dump([exe_data, workout_data], f)

    @staticmethod
    def show_help():
        # show help for this window
        mb.showinfo("Help",
                    "1. Exercises consist of work time and break time for set number of rounds. "
                    "Delay before starting first round can also be set.\n\n"
                    "2. To start the exercise its number of rounds and worktime or breaktime must be greater than zero.\n\n"
                    "3. Exercise can be saved when its name its not empty.\n\n"
                    "4. Workout is a sequence of exercises that are automatically started. "
                    "Additional break between exercises can be inserted as an option in workout.\n\n"
                    "5. Workout can be stopped with reset workout button.")


class ExerciseNotExists(Exception):
    # Custom exception to raise when workout in imported file contains not existing exercise
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
