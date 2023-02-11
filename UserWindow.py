from tkinter import *
from tkinter import messagebox as mb


class UserWindow:
    # parent class for create user window and edit user window
    # creates widgets, checks if inputs are valid

    def __init__(self, root, window, DB):
        self.root = root # login window
        self.window = window
        self.DB = DB
        self.window.geometry('160x240')
        # show login window if create user closed
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Create variables
        self.name_str = StringVar()
        self.email_str = StringVar()
        self.password_str = StringVar()
        self.repeat_password_str = StringVar()

        # Create widgets
        self.name_label = Label(self.window, text='Name:')
        self.name_label.place(x=10, y=10)

        self.name_entry = Entry(self.window, textvariable=self.name_str, highlightthickness=1)
        self.name_entry.place(x=12, y=32)

        self.email_label = Label(self.window, text='e-mail:')
        self.email_label.place(x=10, y=55)

        self.email_entry = Entry(self.window, textvariable=self.email_str, highlightthickness=1)
        self.email_entry.place(x=12, y=77)

        self.password_label = Label(self.window, text='Password:')
        self.password_label.place(x=10, y=100)

        self.password_entry = Entry(self.window, textvariable=self.password_str, show='*', highlightthickness=1)
        self.password_entry.place(x=12, y=122)

        self.repeat_password_label = Label(self.window, text='Repeat Password:')
        self.repeat_password_label.place(x=10, y=145)

        self.repeat_password_entry = Entry(self.window, textvariable=self.repeat_password_str, show='*',
                                           highlightthickness=1)
        self.repeat_password_entry.place(x=12, y=167)

        # check validity of inputs after character is entered
        self.name_str.trace("w", self.is_name_valid)
        self.email_str.trace("w", self.is_email_valid)
        self.password_str.trace("w", lambda x,y,z: self.is_password_valid(self.password_str,
                                self.password_entry))
        self.repeat_password_str.trace("w", lambda x,y,z: self.is_password_valid(self.repeat_password_str,
                                        self.repeat_password_entry))



    def on_closing(self):
        # unhide login window on closing
        self.window.destroy()
        self.root.deiconify()

    def is_name_valid(self, *args):
        # check if name is valid: between 3-40 characters, only alphanumeric return True/False,
        # highlight widget red if input incorrect
        name = self.name_str.get()
        if len(name) < 3 or not name.isalnum() or len(name) > 40:
            # input incorrect, highlight red
            self.name_entry.configure(highlightbackground="red", highlightcolor="red")
            return False
        else:
            # input correct, remove highlight
            self.name_entry.configure(highlightbackground="light grey", highlightcolor="light grey")
            return True

    def is_email_valid(self, *args):
        # check if email is valid: between 3-40 characters, contains 1 @, doesnt contain space, domain contains '.',
        # '.' is not first or last character of the domain and local name, d
        email = self.email_str.get()
        # check for length and presence of @
        if len(email) == 0 or '@' not in email or ' ' in email or len(email) > 40:
            # input incorrect highlight red and return
            self.email_entry.configure(highlightbackground="red", highlightcolor="red")
            return False
        # get here if email contains @
        local, domain = email.split('@')
        # check other conditions
        if email.count('@') != 1 or len(local) == 0 or len(domain) == 0 or '.' not in domain or\
           local[0] == '.' or local[-1] == '.' or domain[0] == '.' or domain[-1] == '.':
            # input incorrect highlight red and return
            self.email_entry.configure(highlightbackground="red", highlightcolor="red")
            return False
        else:
            # input correct remove highlight and return
            self.email_entry.configure(highlightbackground="light grey", highlightcolor="light grey")
            return True

    @staticmethod
    def is_password_valid(str_var, widget, *args):
        # check if password is valid: between 3-40 characters, no spaces, contains at least one number and one letter
        passw = str_var.get()
        num, let = False, False
        # check for presence of one letter and one number
        for p in passw:
            if p.isdecimal():
                num = True
            if p.isalpha():
                let = True
            if num and let:
                break
        # check other condtions
        if len(passw) < 4 or len(passw) > 40 or ' ' in passw or not num or not let:
            # input incorrect highlight red and return
            widget.configure(highlightbackground="red", highlightcolor="red")
            return False
        else:
            # input correct remove highlight and return
            widget.configure(highlightbackground="light grey", highlightcolor="light grey")
            return True

class CreateUserWindow(UserWindow):
    # Creating new user window class allowing to create new user withou loggin in
    def __init__(self, root, window, DB):
        # call init of parent class
        super().__init__(root,window, DB)
        # Add create user button
        self.create_user_btn = Button(self.window, text="Create User", command=self.create_user, width = 12)
        self.create_user_btn.place(x=30, y=200)

    def create_user(self):
        # button function, rechecks all inputs, shows message if they are incorrect,
        # checks if password and reppeat password are the same
        # calls DB function to add user
        if not (self.is_name_valid() and self.is_email_valid() and
                self.is_password_valid(self.password_str, self.password_entry) and
                self.is_password_valid(self.repeat_password_str, self.repeat_password_entry)):
            mb.showerror('Error', 'Incorrect inputs.')
            return
        if self.password_str.get() != self.repeat_password_str.get():
            mb.showerror('Error', 'Repeated password not identical.')
            return
        # If no errors call DB function, res = True if user was successfully created, error = error message if occurred
        res, error = self.DB.add_user(self.name_str.get(), self.email_str.get(), self.password_str.get())
        if res:
            mb.showinfo('Success', 'User successfully created.')
            self.on_closing()
        else:
            mb.showerror('Error', 'Database Error:' + error)


class EditUserWindow(UserWindow):
    # Editing window class which allows to change parameters of currently logged in user
    def __init__(self, root, window, DB, user):
        # call init of parent class
        super().__init__(root,window, DB)
        # add edit button
        self.create_user_btn = Button(self.window, text="Save Data", command=lambda: self.edit_user(user), width = 12)
        self.create_user_btn.place(x=30, y=200)

        # set user name to current user and disable editing
        self.name_str.set(user.name)
        self.name_entry.configure(state=DISABLED)

        # insert current email into email field
        self.email_str.set(user.email)


    def edit_user(self, user):
        # button function, rechecks all inputs, shows message if they are incorrect,
        # checks if password and repeat password are the same
        # calls DB function to edit user
        if not (self.is_name_valid() and self.is_email_valid() and
                self.is_password_valid(self.password_str, self.password_entry) and
                self.is_password_valid(self.repeat_password_str, self.repeat_password_entry)):
            mb.showerror('Error', 'Incorrect inputs.')
            return
        if self.password_str.get() != self.repeat_password_str.get():
            mb.showerror('Error', 'Repeated password not identical.')
            return
        # If no errors call DB function, res = True if user was successfully created, error = error message if occurred
        res, error = self.DB.edit_user(self.name_str.get(), self.email_str.get(), self.password_str.get())
        if res:
            mb.showinfo('Success', 'Data successfully edited.')
            self.window.destroy()
            self.root.deiconify()
            user.change_data([self.email_str.get()])
        else:
            mb.showerror('Error', 'Database Error:' + error)


