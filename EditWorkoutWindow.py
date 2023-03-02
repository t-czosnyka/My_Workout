from tkinter import *
from WorkoutMenu import WorkoutMenu
import tkinter
from tkinter import messagebox as mb


class EditWorkoutWindow:

    def __init__(self, root, frame, DB, user, selected_workout_str: str, workout_processor):
        self.root = root  # gui window
        self.frame = frame
        self.DB = DB
        self.user = user
        self.frame.geometry('300x300')
        # disable resizing
        self.frame.resizable(False, False)
        # show gui window if create user closed
        self.frame.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.dragged_exe = None
        self.allow_workout_list_selection = False
        self.workout_processor = workout_processor

        # Define variables
        self.workout_name_str = StringVar()

        # Create widgets
        self.exe_label = Label(self.frame, text="Exercises:", font=("Helvetica", 13))
        self.exe_label.place(x=150, y=30)

        self.workout_label = Label(self.frame, text="Workout", font=("Helvetica", 16))
        self.workout_label.place(x=10, y=5)

        # validating function for entry widget
        val = self.frame.register(self.user.validate_name_input)

        self.workout_label_name = Entry(self.frame, textvariable=self.workout_name_str, validate='key',
                                        validatecommand=(val, '%P'))
        self.workout_label_name.place(x=10, y=35)

        # create list with current workout
        self.curr_workout_list = Listbox(self.frame, height=7, selectmode=SINGLE, activestyle='none')
        self.curr_workout_list.place(x=10, y=60)

        # create option menu based on user workouts
        self.workout_menu = WorkoutMenu(self.user, self.frame, 10, 183, self.curr_workout_list, False,
                                        self.workout_processor)
        # select previously selected workout after opening new window
        if selected_workout_str != '':
            self.workout_menu.select_workout(selected_workout_str)

        # save workout button
        self.save_workout_btn = Button(self.frame, text="Save Workout", command=self.save_workout, state=DISABLED, width=14)
        self.save_workout_btn.place(x=12, y=242)

        # delete workout button
        self.delete_workout_btn = Button(self.frame, text="Delete Workout", command=self.delete_workout, width=14)
        self.delete_workout_btn.place(x=150, y=242)

        # create list with available exercises
        self.curr_exe_list = Listbox(self.frame, height=10, selectmode=SINGLE, activestyle='none')
        self.curr_exe_list.place(x=150, y=60)
        for i, exe in enumerate(self.user.exercises, 1):
            self.curr_exe_list.insert(i, exe)

        # write selected name into workout name
        self.workout_menu.select_work_str.trace_variable("w", self.select_workout_name)
        self.select_workout_name()
        self.workout_name_str.trace("w", self.validate_inputs)

        ### Drag and drop ###
        # Configuration of drag and drop events
        # Drag exercise when mouse button pressed in curr exe list
        self.curr_exe_list.bind('<ButtonPress-1>', self.drag_exe)
        # Allow highlight of curr workout list when cursor leaves curr exe list and exercise is selected
        self.curr_exe_list.bind('<Leave>', self.allow_highlight)
        # Highlight insertion point in curr workout list
        # when mouse is moved with pressed button and exercise is selected
        self.frame.bind('<B1-Motion>', self.highlight_insertion_exe)
        # Add exercise to curr workout list if button was released inside its borders
        self.frame.bind('<ButtonRelease-1>', self.release_exe)

        # Double click to remove exercise form workout list
        self.curr_workout_list.bind('<Double-Button-1>', self.remove_exe)

        # Create help menu
        # Create menubar
        self.menubar = Menu(self.frame)
        self.frame.config(menu=self.menubar)
        # Create menu
        self.help_menu = Menu(self.menubar, tearoff=0)
        # Add command
        self.help_menu.add_command(label="Help", command=self.show_help)
        # Add cascacde
        self.menubar.add_cascade(label="Help", menu=self.help_menu)
    def select_workout_name(self,*args):
        # if workout selected from menu write name into variable
        self.workout_name_str.set(self.workout_menu.select_work_str.get())
        self.validate_inputs()

    def on_closing(self):
        # unhide gui window on closing
        self.frame.destroy()
        self.root.deiconify()


    def drag_exe(self, *args):
        # drag exercise from curr exe list
        # assign exercise based on y position of a mouse cursor inside the curr exe list
        if self.curr_exe_list.size() == 0:
            return
        index = self.curr_exe_list.nearest(args[0].y)
        # drag the nearest item to cursor y position
        # if position is below lowest item border - assign nothing
        if args[0].y <= self.row_low_border_pos(self.curr_exe_list, index):
            self.dragged_exe = self.curr_exe_list.get(index)
            self.allow_workout_list_selection = False


    def release_exe(self, *args):
        # When mouse button is released check its position
        # If exercise is dragged and release position is inside curr workout list - add exercise to current workout
        # If release position is outside clear dragged exercise
        if self.dragged_exe is None:
            return
        # check if cursor is inside curr_workout_list
        x = self.frame.winfo_pointerx() - self.frame.winfo_rootx()
        y = self.frame.winfo_pointery() - self.frame.winfo_rooty()
        if self.check_cursor_pos(self.curr_workout_list, x, y):
            # cursor inside - insert dragged exercise into curr workout list
            self.drop_exe(y - self.curr_workout_list.winfo_y())
        else:
            # cursor outside - clear dragged exercise
            self.dragged_exe = None
            self.allow_workout_list_selection = False

    def highlight_insertion_exe(self, *args):
        # highlight insertion point in workout exe list while dragging element
        if self.dragged_exe is not None and self.allow_workout_list_selection:
            index = self.curr_workout_list.nearest(args[0].y)
            self.curr_workout_list.selection_clear(0, END)
            self.curr_workout_list.selection_set(index)
            self.curr_workout_list.selection_anchor(index)

    def allow_highlight(self, *args):
        # allow highlighting of curr workout list if cursor leave curr exe list and exercise is dragged
        if self.dragged_exe is not None:
            self.allow_workout_list_selection = True

    def drop_exe(self, cursor_y_pos):
        # add exercise to curr workout list when mouse button is released inside it
        # index - insert point of new exercise, based od mouse cursor y position
        index = self.curr_workout_list.nearest(cursor_y_pos)
        # if cursor lower than the lowest row, increment index to add exercise at the end
        # compare cursor y position to border of the lowest row
        if self.curr_workout_list.size() > 0 and cursor_y_pos > self.row_low_border_pos(self.curr_workout_list, index):
            index += 1

        # insert dragged exercise and set selection to it
        self.curr_workout_list.insert(index, self.dragged_exe)
        self.curr_workout_list.selection_clear(0, END)
        self.curr_workout_list.see(index)
        self.curr_workout_list.selection_set(index)
        self.curr_workout_list.selection_anchor(index)

        # clear dragged exercise and selection marker
        self.dragged_exe = None
        self.allow_workout_list_selection = False
        self.validate_inputs()

    def remove_exe(self, *args):
        # remove exercise from curr workout list by double click
        # remove the nearest row from cursor y position
        # if double click below lowest row - dont remove
        if self.curr_workout_list.size() == 0:
            return
        index = self.curr_workout_list.nearest(args[0].y)
        # compare cursor y position to border of the lowest row
        if args[0].y > self.row_low_border_pos(self.curr_workout_list,index):
            return
        self.curr_workout_list.delete(index)
        self.validate_inputs()

    @staticmethod
    def row_low_border_pos(listbox: Listbox, index):
        # calculate position of lower border of listbox row indicated by index
        bbox = listbox.bbox(index)
        return bbox[1] + bbox[3]

    @staticmethod
    def check_cursor_pos(widget: Widget, cursor_pos_x, cursor_pos_y):
        # check if cursor is currently inside a widget
        # all positions relative to top corner of current window
        inside = True
        # check if inside in x-axis
        if not(widget.winfo_x() <= cursor_pos_x <= widget.winfo_x() + widget.winfo_width()):
            inside = False
        # check if inside in y-axis
        if not(widget.winfo_y() <= cursor_pos_y <= widget.winfo_y() + widget.winfo_height()):
            inside = False
        return inside

    def validate_inputs(self, *args):
        # check if workout name and exercise list are not empty
        if len(self.workout_name_str.get()) > 0 and self.curr_workout_list.size() > 0:
            self.save_workout_btn.configure(state=NORMAL)
            return True
        else:
            self.save_workout_btn.configure(state=DISABLED)
            return False


    def save_workout(self):
        # Edit or create new workout in DB and user data
        if not self.validate_inputs():
            return
        exercises = list(self.curr_workout_list.get(0,END))
        # Call DB function to add workout
        res, error = self.DB.save_workout(self.user.name, self.workout_name_str.get(), exercises,
                                          self.user.get_str_var(self.workout_menu.workout_break_sec_str))
        if not res:
            # Display message
            mb.showerror("Database Error.", error)
            return
        self.user.save_workout(self.workout_name_str.get(), exercises,
                               self.user.get_str_var(self.workout_menu.workout_break_sec_str))
        self.user.req_workout_update_set()
        self.workout_menu.select_workout(self.workout_name_str.get())
        self.workout_menu.update_menu()
        # Display message
        mb.showinfo('Success', 'Workout saved.')



    def delete_workout(self):
        workout_name = self.workout_name_str.get()
        if len(workout_name) == 0:
            mb.showerror("Error.", "Workout name cannot be empty.")
            return
        # delete from DB
        res, error = self.DB.delete_workout(self.user.name, workout_name)
        # check if deleted correctly if not return
        if not res:
            # Display message
            mb.showerror("Database Error.", error)
            return
        # deleted workout from user data
        self.user.delete_workout(workout_name)
        # delete current name from select menu
        self.workout_menu.select_work_str.set('')
        self.user.req_workout_update_set()
        self.workout_menu.update_menu()
        # Display message
        mb.showinfo('Success', 'Workout deleted.')

    @staticmethod
    def show_help():
        # show help for this window
        mb.showinfo("Help", "1. Drag and drop exercises from exercises list into the workout list.\n"
                            "2. Double click exercise to remove it from workout list.\n"
                            "3. Workout name cannot be empty.\n"
                            "4. Extra break is added between exercises.")



