from tkinter import *
from DB import DB

class Login:

    def __init__(self, top, root, DB):
        self.DB = DB
        self.root = root
        self.top = top
        self.top.geometry('250x100')

        # tkinter variables
        self.password_str = StringVar()
        self.login_str = StringVar()

        # initialize variables
        self.password_str.set('')
        self.login_str.set('')

        #create widgets
        self.login_label = Label(self.top,text='Login:')
        self.login_label.place(x=10,y=10)
        self.password_label = Label(self.top,text='Password:')
        self.password_label.place(x=10, y=30)
        self.login = Entry(self.top,textvariable=self.login_str)
        self.login.place(x=90, y=10)
        self.password = Entry(self.top,textvariable=self.password_str,show='*')
        self.password.place(x=90, y=30)

        self.login_button = Button(self.top,text="Login", command=self.validate)
        self.login_button.place(x=100,y=60)
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

    def validate(self):
        if self.DB.validate(self.login_str.get(), self.password_str.get()):
            self.log_on()
        else:
            print("Wrong login or password")
        self.password_str.set('')


    def log_on(self):
        self.root.deiconify()
        self.top.destroy()

    def on_closing(self):
        self.top.destroy()
        self.root.destroy()

