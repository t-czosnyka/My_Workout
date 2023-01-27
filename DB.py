import mysql.connector
from User import User
from Exercise import Exercise
class DB:

    def __init__(self):
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
                          name VARCHAR(40), time_work INT, time_rest INT, num_rounds INT, delay INT,\
                          FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

        mycursor.execute("CREATE TABLE IF NOT EXISTS work_users (work_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                          name  VARCHAR(40),\
                          FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

        mycursor.execute("CREATE TABLE IF NOT EXISTS work_exes (work_id INT, exe_id INT, order_num INT,\
                         FOREIGN KEY (work_id) REFERENCES work_users(work_id) ON DELETE CASCADE,\
                         FOREIGN KEY (exe_id) REFERENCES exercises(exe_id) ON DELETE CASCADE,\
                         PRIMARY KEY(work_id, exe_id, order_num))")

        my_db.close()

    def validate(self, in_login, in_password):
        valid = False
        login_found = False
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Batman123",
            database="my_workout_db"
        )
        mycursor = my_db.cursor()
        # get logins from DB
        mycursor.execute("SELECT name FROM users")
        logins = mycursor.fetchall()
        # compare logins with inserted login
        for login in logins:
            if login[0] == in_login:
                login_found = True
        # if login is in DB compare password
        if login_found:
            # get password from DB
            mycursor.execute(f"SELECT password FROM users WHERE name = '{in_login}'")
            password = mycursor.fetchall()
            valid = password[0][0] == in_password
        my_db.close()
        return valid

    def get_user(self,user_name):
        # Create and return User object with data from DB
        exercises = self.get_exercises(user_name)
        user = User(user_name,False,exercises)
        return user

    def save_exercise(self, user_name, exe_name, worktime, breaktime, num_rounds, delay):
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Batman123",
            database="my_workout_db"
        )
        mycursor = my_db.cursor()
        mycursor.execute(f"INSERT INTO exercises ('user_id', 'name','time_work','time_rest','num_rounds','delay') VALUES((SELECT user_id FROM users WHERE name='{user_name}'),\
                         '{exe_name}',{worktime},{breaktime},{num_rounds},{delay}")
        result = mycursor.fetchall()
        print(result)
        my_db.close()

    def get_exercises(self,user_name):
        # Get exercises data from DB for user
        exercises ={}
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Batman123",
            database="my_workout_db"
        )
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT name,time_work,time_rest,num_rounds,delay FROM exercises WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')")
        exes = mycursor.fetchall()
        for exe in exes:
            exercises[exe[0]] = Exercise(exe[0],exe[1],exe[2],exe[3],exe[4])
        my_db.close()
        return exercises