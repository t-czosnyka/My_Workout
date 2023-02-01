import mysql.connector
from User import User
from Exercise import Exercise
class DB:
    # DB class handles database operations using mysql connector
    def __init__(self):
        self.error = False
        self.error_msg = ''
        try:
            my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Batman123"
            )
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err
            return

        mycursor = my_db.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS my_workout_db;")
        # Disconnecting from the server
        my_db.close()
        my_db = self.connect_to_DB()
        # end function if error happens during connection
        if not my_db:
            return

        mycursor = my_db.cursor()
        # Create tables if they dont exist
        mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,\
                           name VARCHAR(40), email VARCHAR(40), password VARCHAR(40),\
                         UNIQUE(name))")

        mycursor.execute("CREATE TABLE IF NOT EXISTS exercises (exe_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                          name VARCHAR(40), time_work INT, time_rest INT, num_rounds INT, delay INT,\
                          UNIQUE(user_id,name), FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

        mycursor.execute("CREATE TABLE IF NOT EXISTS work_users (work_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                          name  VARCHAR(40),\
                          FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

        mycursor.execute("CREATE TABLE IF NOT EXISTS work_exes (work_id INT, exe_id INT, order_num INT,\
                         FOREIGN KEY (work_id) REFERENCES work_users(work_id) ON DELETE CASCADE,\
                         FOREIGN KEY (exe_id) REFERENCES exercises(exe_id) ON DELETE CASCADE,\
                         PRIMARY KEY(work_id, exe_id, order_num))")
        # Create test user if doesnt exist
        mycursor.execute("INSERT INTO users (name, email, password) VALUES('test','test@test.com','t1234')\
                         ON DUPLICATE KEY UPDATE user_id = user_id")

        # Create test exercise if doesnt exist
        mycursor.execute("INSERT INTO exercises (user_id, name, time_work, time_rest, num_rounds, delay)\
                         VALUES((SELECT user_id FROM users WHERE name = 'test'),'test_exe',60,20,3,10)\
                         ON DUPLICATE KEY UPDATE exe_id = exe_id")
        my_db.commit()
        my_db.close()

    def connect_to_DB(self):
        # connecting to the database, return connection object if succesful, return None if error
        try:
            my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Batman123",
                database="my_workout_db"
            )
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err
            return None
        else:
            return my_db

    def validate(self, in_login, in_password):
        valid = False
        login_found = False
        my_db = self.connect_to_DB()
        if not my_db:
            return

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
        error = ''
        my_db = self.connect_to_DB()
        if not my_db:
            return False, error
        result = False
        mycursor = my_db.cursor()
        try:
            mycursor.execute(f"INSERT INTO exercises (user_id, name,time_work,time_rest,num_rounds,delay) \
                             VALUES((SELECT user_id FROM users WHERE name='{user_name}'),\
                             '{exe_name}',{worktime},{breaktime},{num_rounds},{delay})\
                             ON DUPLICATE KEY UPDATE time_work={worktime},time_rest={breaktime},\
                             num_rounds={num_rounds},delay={delay}")
        except mysql.connector.Error as err:
            error = err
        else:
            #No error
            result = True
        my_db.commit()
        my_db.close()
        return result, error

    def get_exercises(self,user_name):
        # Get exercises data from DB for user
        exercises ={}
        my_db = self.connect_to_DB()
        if not my_db:
            return exercises
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT name,time_work,time_rest,num_rounds,delay FROM exercises WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')")
        exes = mycursor.fetchall()
        for exe in exes:
            exercises[exe[0]] = Exercise(exe[0],exe[1],exe[2],exe[3],exe[4])
        my_db.close()
        return exercises

    def delete_exercise(self,user_name,exe_name):
        # delete exercise from DB
        error = ''
        my_db = self.connect_to_DB()
        if not my_db:
            return False, error
        mycursor = my_db.cursor()
        res = False
        mycursor.execute(f"SELECT * FROM exercises \
                         WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}') AND name='{exe_name}'")
        exe = mycursor.fetchall()
        if len(exe) == 0:
            return False, 'Exercise not found.'
        try:
            mycursor.execute(f"DELETE FROM exercises  \
                             WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}') AND name='{exe_name}'")
            my_db.commit()
        except mysql.connector.Error as err:
            error = err
        else:
            res = True
        my_db.close()
        return res, error
