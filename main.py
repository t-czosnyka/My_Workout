# importing required libraries
from tkinter import *
from Login import Login
from DB import DB


if __name__ == '__main__':
    my_db = DB()            # Initialize database
    root = Tk()
    Login(root, my_db)          # Create login window
    root.mainloop()








