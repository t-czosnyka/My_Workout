# importing required libraries
from tkinter import *
from Login import Login
from DB import DB


def main():
    my_db = DB()  # Initialize database
    root = Tk()     # root window
    Login(root, my_db)  # Create login window
    root.mainloop()     # Tkinter main loop


if __name__ == '__main__':
    main()






