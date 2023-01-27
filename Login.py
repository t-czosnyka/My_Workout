from tkinter import *
from DB import DB
from Gui import Gui

class Login:

    def __init__(self, root, DB):
        self.DB = DB
        self.root = root
        self.root.geometry('250x110')

        # tkinter variables
        self.password_str = StringVar()
        self.login_str = StringVar()

        # initialize variables
        self.password_str.set('')
        self.login_str.set('')

        #create widgets
        self.login_label = Label(self.root,text='Login:')
        self.login_label.place(x=10,y=10)
        self.password_label = Label(self.root,text='Password:')
        self.password_label.place(x=10, y=30)
        self.login = Entry(self.root,textvariable=self.login_str)
        self.login.place(x=90, y=10)
        self.password = Entry(self.root,textvariable=self.password_str,show='*')
        self.password.place(x=90, y=30)

        self.login_button = Button(self.root,text="Login", command=self.validate)
        self.login_button.place(x=100,y=60)
        self.msg = Label(self.root, text="")



    def validate(self):
        if self.DB.validate(self.login_str.get(), self.password_str.get()):
            self.login_str.set('')
            self.password_str.set('')
            self.log_on(self.login_str.get())
            self.msg.destroy()
        else:
            self.password_str.set('')
            self.msg = Label(self.root, text="Wrong login or password", fg='Red')
            self.msg.place(x=50, y=87)


    def log_on(self, login):
        self.root.withdraw()
        frame = Toplevel()
        user = self.DB.get_user(login)
        gui = Gui(self.root, frame, user, self.DB)
        gui.update()




