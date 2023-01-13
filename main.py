# importing required libraries
import mysql.connector
from User import User
from Timer import Timer
from time import sleep
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

    return my_db, mycursor


if __name__ == '__main__':
    my_db, mycursor = init_db()
    mycursor.execute("DESCRIBE users")
    myresult = mycursor.fetchall()
    my_db.close()
    user = User('admin','aaa', 'bbb', True)
    timer = Timer()
    quit, p1 = False, False
    while not quit:                  # main loop


        timer.timing_function(10,True,False)





