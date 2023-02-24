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

    # my_db = mysql.connector.connect(
    #     host="sql.freedb.tech",
    #     user="freedb_my_workout_user",
    #     passwd="Ne8KzVs&2MFsC?r",
    #     database="freedb_my_workout_db",
    #     port=3306
    # )
    # mycursor = my_db.cursor()
    # mycursor.execute("SHOW TABLES")
    # print(mycursor.fetchall())
    # #mycursor.execute("CREATE TABLE test2 (id INT)")
    # my_db.commit()
    # mycursor.execute("DESCRIBE test2")
    # print(mycursor.fetchall())
    # my_db.close()






