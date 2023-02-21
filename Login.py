from tkinter import *
from DB import DB
from Gui import Gui
from UserWindow import CreateUserWindow
from tkinter import messagebox as mb

class Login:
    # class handles login screen and creates Gui and User objects on successful login
    def __init__(self, root, DB):
        self.DB = DB
        self.root = root
        self.root.geometry('250x110')
        # disable resizing
        self.root.resizable(False, False)

        # tkinter variables
        self.password_str = StringVar()
        self.login_str = StringVar()
        self.msg_str = StringVar()

        # initialize variables
        self.password_str.set('')
        self.login_str.set('')
        self.msg_str.set('')

        # create widgets
        self.login_label = Label(self.root,text='Login:')
        self.login_label.place(x=10,y=10)
        self.password_label = Label(self.root,text='Password:')
        self.password_label.place(x=10, y=30)
        self.login = Entry(self.root,textvariable=self.login_str)
        self.login.place(x=90, y=10)
        self.password = Entry(self.root,textvariable=self.password_str,show='*')
        self.password.place(x=90, y=30)

        # Login Button
        self.login_btn = Button(self.root, text="Login", command=self.validate, width=10)
        self.login_btn.place(x=40, y=60)

        # Create User Button
        self.create_user_btn = Button(self.root, text="Create User", command=self.create_user_window, width=10)
        self.create_user_btn.place(x=130, y=60)

        # Status Msg Label
        self.msg = Label(self.root, textvariable=self.msg_str, fg='Red')
        self.msg.place(x=50, y=87)

        # if DB not connected properly display msg and block login button
        if self.DB.error:
            self.msg_str.set('Database connection error!')
            self.login_btn.configure(state=DISABLED)
            self.create_user_btn.configure(state=DISABLED)
    def validate(self):
        # validate login and password in the database, show error message if not correct
        if self.DB.validate(self.login_str.get(), self.password_str.get()):
            login = self.login_str.get()
            self.login_str.set('')
            self.password_str.set('')
            self.log_on(login)
            self.msg_str.set('')
        else:
            self.password_str.set('')
            self.msg_str.set('Wrong login or password.')

    def log_on(self, login):
        # Create User and Gui objects with data from DB on successful login
        user = self.DB.get_user(login)
        # If user was successfully created close login window and Create GUI
        if user is not None:
            frame = Toplevel()
            # Hide login screen
            self.root.withdraw()
            Gui(self.root, frame, user, self.DB)
        else:
            mb.showerror("Error", "Failed to get user data from DB.")

    def create_user_window(self):
        # Create a new window
        self.root.withdraw()
        window = Toplevel()
        CreateUserWindow(self.root, window, self.DB)










