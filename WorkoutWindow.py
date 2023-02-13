from tkinter import *
from Menu import Menu
import tkinter


class WorkoutWindow:

    def __init__(self, root, window, DB, user):
        self.root = root # gui window
        self.window = window
        self.DB = DB
        self.user = user
        self.window.geometry('300x300')
        # show gui window if create user closed
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.dragged_exe = None
        self.allow_workout_list_selection = False

        # Define variables
        self.workout_name_str = StringVar()
        self.workout_break_sec_str = StringVar()

        # Initialize variables
        self.workout_break_sec_str.set('0')

        # Create widgets
        self.exe_label = Label(self.window, text="Exercises:", font=("Helvetica", 13))
        self.exe_label.place(x=150, y=30)

        self.workout_label = Label(self.window, text="Workout", font=("Helvetica", 16))
        self.workout_label.place(x=10, y=5)

        self.workout_label_name = Entry(self.window, textvariable=self.workout_name_str)
        self.workout_label_name.place(x=10, y=35)

        self.workout_break_sec_label = Label(self.window, text="Extra break[sec]:")
        self.workout_break_sec_label.place(x=150, y=180)

        self.workout_break_sec = Entry(self.window, textvariable=self.workout_break_sec_str, width=4)
        self.workout_break_sec.place(x=153, y=205)

        # create list with current workout
        self.curr_workout_list = Listbox(self.window, height=7, selectmode=SINGLE, activestyle='none')
        self.curr_workout_list.place(x=10, y=60)

        # create option menu based on user workouts
        self.workout_menu = Menu(self.user, self.window, 10, 180, self.curr_workout_list)
        self.workout_menu.create_workout_menu()

        # save exercise button
        self.save_btn = Button(self.window, text="Save Workout", command=self.save_workout, state=DISABLED, width=14)
        self.save_btn.place(x=12, y=212)

        # delete exercise button
        self.delete_btn = Button(self.window, text="Delete Workout", command=self.delete_workout, width=14)
        self.delete_btn.place(x=12, y=242)

        # create list with available exercises
        self.curr_exe_list = Listbox(self.window, height=7, selectmode=SINGLE, activestyle='none')
        self.curr_exe_list.place(x=150, y=60)
        for i, exe in enumerate(self.user.exercises, 1):
            self.curr_exe_list.insert(i, exe)

        # write selected name into workout name
        self.workout_menu.select_work_str.trace_variable("w", self.select_workout_name)
        self.select_workout_name()

        ### Drag and drop ###
        # Configuration of drag and drop events
        # Drag exercise when mouse button pressed in curr exe list
        self.curr_exe_list.bind('<ButtonPress-1>', self.drag_exe)
        # Allow highlight of curr workout list when cursor leaves curr exe list and exercise is selected
        self.curr_exe_list.bind('<Leave>', self.allow_highlight)
        # Highlight insertion point in curr workout list
        # when mouse is moved with pressed button and exercise is selected
        self.window.bind('<B1-Motion>', self.highlight_insertion_exe)
        # Add exercise to curr workout list if button was released inside its borders
        self.window.bind('<ButtonRelease-1>', self.release_exe)

        # Double click to remove exercise form workout list
        self.curr_workout_list.bind('<Double-Button-1>', self.remove_exe)

    def select_workout_name(self,*args):
        # if workout selected from menu write name into variable
        self.workout_name_str.set(self.workout_menu.select_work_str.get())

    def on_closing(self):
        # unhide gui window on closing
        self.window.destroy()
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
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
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


    def save_workout(self):
        pass

    def delete_workout(self):
        pass


