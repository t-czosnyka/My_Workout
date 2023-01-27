# importing required libraries
from tkinter import *
from Login import Login
from Gui import Gui
from User import User
from DB import DB


if __name__ == '__main__':
    my_db = DB()            #Initialize database
    root = Tk()
    Login(root, my_db)          #Create login window
    my_db.get_exercises('tom')
    root.mainloop()








