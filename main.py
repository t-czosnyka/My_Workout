# importing required libraries
import mysql.connector
from User import User
from Exercise import Exercise
from tkinter import *
def init_db():
    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Batman123"
    )

    mycursor = my_db.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS my_workout_db;")

    # Disconnecting from the server
    my_db.close()

    my_db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Batman123",
        database="my_workout_db"
    )
    mycursor = my_db.cursor()

    mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,\
                      name VARCHAR(40), email VARCHAR(40), password VARCHAR(40))")

    mycursor.execute("CREATE TABLE IF NOT EXISTS exercises (exe_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                     name VARCHAR(40), num_rounds INT, time_work INT, time_rest INT, delay INT,\
                     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

    mycursor.execute("CREATE TABLE IF NOT EXISTS work_users (work_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                     name  VARCHAR(40),\
                     FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

    mycursor.execute("CREATE TABLE IF NOT EXISTS work_exes (work_id INT, exe_id INT, order_num INT,\
                    FOREIGN KEY (work_id) REFERENCES work_users(work_id) ON DELETE CASCADE,\
                    FOREIGN KEY (exe_id) REFERENCES exercises(exe_id) ON DELETE CASCADE,\
                    PRIMARY KEY(work_id, exe_id, order_num))")

    my_db.close()
    return

def update():
    global start_btn
    #load_exercise()
    #user.check_exe()
    #if user.valid_exe:
        #start_btn.configure(state=NORMAL)
    #else:
        #start_btn.configure(state=DISABLED)

    user.run_exe()
    if user.curr_exe.finished:
        pause_timer()
        user.reset_exe()

    timer_value_str.set(user.my_timer.time_str)
    round_num_int.set(user.curr_round)
    curr_mode_str.set(user.mode)
    if user.mode == 'Delay' or user.mode == 'Break':
        mode_text.configure(fg="red")
        round_text.configure(fg="red")
        timer_text.configure(fg="red")
    else:
        mode_text.configure(fg="green")
        round_text.configure(fg="green")
        timer_text.configure(fg="green")
    root.after(100, update)

def start_timer():
    global start_btn
    user.running = True
    start_btn.configure(text="Pause",command=pause_timer)

def pause_timer():
    global start_btn
    user.running = False
    start_btn.configure(text="Start", command=start_timer)

def reset_exercise():
    pause_timer()
    user.reset_exe()
    load_exercise()

def get_str_var(str_var):
    #return int of stringvar or 0 if empty
    if str_var.get() != '':
        return int(str_var.get())
    else:
        return 0

def get_inputs():
    # get inputs from exercise entry widgets
    work_time = get_str_var(work_time_min_str) * 60 + get_str_var(work_time_sec_str)
    break_time = get_str_var(break_time_min_str) * 60 + get_str_var(break_time_sec_str)
    num_rounds = get_str_var(num_rounds_str)
    delay = get_str_var(delay_time_sec_str)
    return [work_time, break_time, num_rounds, delay]


def load_exercise():
    # load values from entry widgets to current exercise
    if not user.curr_exe.started and not user.curr_exe.finished:
            inputs = get_inputs()
            user.curr_exe.worktime = inputs[0]
            user.curr_exe.breaktime = inputs[1]
            user.curr_exe.num_rounds = inputs[2]
            user.curr_exe.delay = inputs[3]
            user.check_exe()
            if user.valid_exe:
                start_btn.configure(state=NORMAL)
            else:
                start_btn.configure(state=DISABLED)




def value_changed(var,index,mode):
    #check values when entry widgest are changed
    load_exercise()


def gui():

    global curr_mode_str
    global timer_value_str
    global round_num_int
    global start_btn
    global mode_text
    global timer_text
    global round_text

    global work_time_min_str
    global work_time_sec_str
    global break_time_min_str
    global break_time_sec_str
    global delay_time_sec_str
    global num_rounds_str
    global exercise_name_str

    global select_exe_menu



    curr_mode_str = StringVar()
    timer_value_str = StringVar()
    round_num_int = IntVar()
    color_str = StringVar()

    #Entry widget variables:
    work_time_min_str = StringVar()
    work_time_sec_str = StringVar()

    break_time_min_str = StringVar()
    break_time_sec_str = StringVar()

    num_rounds_str = StringVar()
    exercise_name_str = StringVar()

    delay_time_sec_str = StringVar()
    select_exe_str = StringVar()

    #Initialize tkinter variables
    timer_value_str.set(user.my_timer.time_str)
    round_num_int.set(user.curr_round)
    curr_mode_str.set(user.mode)
    color_str.set("Green")

    work_time_min_str.set('0')
    work_time_sec_str.set('0')

    break_time_min_str.set('0')
    break_time_sec_str.set('0')

    num_rounds_str.set('0')

    delay_time_sec_str.set('0')

    select_exe_str.set('')

    #Create widgets
    mode_text = Label(root, textvariable=curr_mode_str, font=("Helvetica", 40), fg=color_str.get())
    mode_text.grid(row=0, column=0, padx=(10,0), columnspan=4)
    timer_text = Label(root, textvariable=timer_value_str, font=("Helvetica", 80),  fg=color_str.get())
    timer_text.grid(row=1, column=0, columnspan=3,padx=10)
    round_text = Label(root, textvariable=round_num_int,  font=("Helvetica", 40),  fg=color_str.get())
    round_text.grid(row=1, column=4, padx=10)

    start_btn = Button(root, text="Start", command=start_timer,width=20,height=2,state=DISABLED)
    start_btn.grid(row=2, column=0, columnspan=2)

    reset_btn = Button(root, text="Reset", command=reset_exercise,width=20,height=2)
    reset_btn.grid(row=2, column=2, columnspan=2)

    exe_label = Label(root, text="Exercise", font=("Helvetica", 20))
    exe_label.grid(row=3, column=0,columnspan=2,pady=(10,0))

    workout_label = Label(root, text="Workout", font=("Helvetica", 20))
    workout_label.grid(row=3, column=2,columnspan=2,pady=(10,0))

    exe_name_label = Label(root, text="Exercise name:", font=("Helvetica", 10))
    exe_name_label.grid(row=4, column=0, sticky='w', padx=(20, 0))

    work_time_label = Label(root, text="Work time:[min][sec]", font=("Helvetica", 10))
    work_time_label.grid(row=5, column=0, sticky='w', padx=(20,0))

    break_time_label = Label(root, text="Break time:[min][sec]", font=("Helvetica", 10))
    break_time_label.grid(row=6, column=0,  sticky='w', padx=(20,0))

    num_rounds_label = Label(root, text="No. of rounds:", font=("Helvetica", 10))
    num_rounds_label.grid(row=7, column=0,  sticky='w', padx=(20,0))

    delay_time_label = Label(root, text="Delay time:[sec]", font=("Helvetica", 10))
    delay_time_label.grid(row=8, column=0,  sticky='w', padx=(20,0))

    def save_exercise():
        # save button function
        # save entry widget values into Exercise object
        name = exercise_name_str.get()
        inputs = get_inputs()
        if name in user.exercises:
            user.exercises[name].worktime = inputs[0]
            user.exercises[name].breaktime = inputs[1]
            user.exercises[name].num_rounds = inputs[2]
            user.exercises[name].delay = inputs[3]
        else:
            user.exercises[name] = Exercise(name, *inputs)
        update_option_menu()

    def is_val_dig(input):   # validating function for entry widgets, max two digits allowed
        if (input.isdigit() or input == '') and len(input) <= 2:
            return True
        else:
            return False

    def is_val_str(input):  #validate exercise name - no more than 20 characters
        if len(input) <= 20:
            return True
        else:
            return False

    def exe_name(var,index,mode):
        # possible to save exercise only if name is inserted
        if exercise_name_str.get() != '':
            save_btn.configure(state=NORMAL)
        else:
            save_btn.configure(state=DISABLED)

    def update_option_menu():
        global select_exe_menu
        # after adding new exercise recreate OptionMenu widget with new options
        select_exe_menu.destroy()
        select_exe_menu = OptionMenu(root, select_exe_str, *user.exercises.keys(), command=select_exe)
        select_exe_menu.place(x=120, y=392)

    def select_exe(selected):
        #insert selected values into entry widgets
        print("selected",selected)
        if selected in user.exercises:
            exercise_name_str.set(user.exercises[selected].name)
            work_time_min_str.set(str(user.exercises[selected].worktime//60))
            work_time_sec_str.set(str(user.exercises[selected].worktime%60))
            break_time_min_str.set(str(user.exercises[selected].breaktime//60))
            break_time_sec_str.set(str(user.exercises[selected].breaktime%60))
            num_rounds_str.set(str(user.exercises[selected].num_rounds))
            delay_time_sec_str.set(str(user.exercises[selected].delay))

    reg = root.register(is_val_dig)
    reg2 = root.register(is_val_str)

    exercise_name = Entry(root,width=15,validate="key",validatecommand=(reg2,'%P'), textvariable=exercise_name_str)
    exercise_name.place(x=150, y= 283)

    exercise_name_str.trace_add("write",exe_name)


    work_time_min = Entry(root, validate="key",validatecommand=(reg,'%P'),width=5,textvariable=work_time_min_str)
    work_time_min.place(x=150, y= 305)

    work_time_sec = Entry(root, validate="key",validatecommand=(reg,'%P'),width=5,textvariable=work_time_sec_str)
    work_time_sec.place(x=210, y= 305)

    break_time_min = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,textvariable=break_time_min_str)
    break_time_min.place(x=150, y=327)

    break_time_sec = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5,textvariable=break_time_sec_str)
    break_time_sec.place(x=210, y=327)

    num_rounds = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5, textvariable=num_rounds_str)
    num_rounds.place(x=150, y=349)

    delay_time_sec = Entry(root, validate="key", validatecommand=(reg, '%P'), width=5, textvariable=delay_time_sec_str)
    delay_time_sec.place(x=150, y=371)

    #trace changes in entry widgets
    work_time_min_str.trace_add("write", value_changed)
    work_time_sec_str.trace_add("write", value_changed)
    break_time_min_str.trace_add("write", value_changed)
    break_time_sec_str.trace_add("write", value_changed)
    num_rounds_str.trace_add("write", value_changed)
    delay_time_sec_str.trace_add("write", value_changed)

    #save button
    save_btn = Button(root,text="Save Exercise",command=save_exercise,state=DISABLED)
    save_btn.place(x=20,y=394)

    #select previously saved exercise from drop down menu
    select_exe_menu = OptionMenu(root, select_exe_str, *user.exercises.keys(), command=select_exe)
    select_exe_menu.place(x=120, y=392)





if __name__ == '__main__':
    init_db()
    root = Tk()
    root.geometry('500x600')


    user = User('admin','aaa', 'bbb', True)
    gui()
    update()
    root.mainloop()








