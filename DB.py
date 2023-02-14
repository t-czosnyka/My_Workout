import mysql.connector
from User import User
from Exercise import Exercise
from Workout import Workout
from itertools import groupby
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
                          name  VARCHAR(40), extra_break_sec INT DEFAULT 0, UNIQUE(user_id,name),\
                          FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)")

        mycursor.execute("CREATE TABLE IF NOT EXISTS work_exes (work_id INT, exe_id INT, order_num INT, \
                         UNIQUE(work_id, order_num),\
                         FOREIGN KEY (work_id) REFERENCES work_users(work_id) ON DELETE CASCADE,\
                         FOREIGN KEY (exe_id) REFERENCES exercises(exe_id) ON DELETE CASCADE,\
                         PRIMARY KEY(work_id, exe_id, order_num))")
        # Create test user if doesnt exist
        mycursor.execute("INSERT INTO users (name, email, password) VALUES('test','test@test.com','t1234')\
                         ON DUPLICATE KEY UPDATE user_id = user_id")

        mycursor.execute("INSERT INTO users (name, email, password) VALUES('test2','test@test.com','1234')\
                                 ON DUPLICATE KEY UPDATE user_id = user_id")

        my_db.commit()
        my_db.close()

        # Create test exercises
        self.save_exercise('test', 'test_exe', 10, 5, 2, 5)
        self.save_exercise('test', 'test_exe2', 9, 4, 1, 4)
        self.save_exercise('test', 'no_work', 20, 10, 5, 5)
        self.save_exercise('test2', 'test2_exe', 8, 4, 1, 3)
        self.save_exercise('test2', 'test2_exe2', 6, 2, 2, 2)
        self.add_workout('test', 'test_workout', ['test_exe','test_exe2'],0)
        self.add_workout('test', 'test2_workout', ['test_exe2','test_exe'],5)
        self.add_workout('test2', 'test2_workout', ['test2_exe','test2_exe2'],10)

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
        workouts = self.get_workouts(user_name)
        data = self.get_user_data(user_name)
        user = User(user_name, exercises, workouts, *data,)
        return user

    def save_exercise(self, user_name, exe_name, worktime_sec, breaktime_sec, num_rounds, delay_sec):
        error = ''
        my_db = self.connect_to_DB()
        if not my_db:
            return False, error
        result = False
        mycursor = my_db.cursor()
        try:
            mycursor.execute(f"INSERT INTO exercises (user_id, name,time_work,time_rest,num_rounds,delay) \
                             VALUES((SELECT user_id FROM users WHERE name='{user_name}'),\
                             '{exe_name}',{worktime_sec},{breaktime_sec},{num_rounds},{delay_sec})\
                             ON DUPLICATE KEY UPDATE time_work={worktime_sec},time_rest={breaktime_sec},\
                             num_rounds={num_rounds},delay={delay_sec}")
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
        # Connect to DB, if connection fails, return empty dict
        my_db = self.connect_to_DB()
        if not my_db:
            return exercises
        # If connection is successful run mysql query
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT name,time_work,time_rest,num_rounds,delay FROM exercises \
                            WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')")
        exes = mycursor.fetchall()
        for exe in exes:
            exercises[exe[0]] = Exercise(exe[0],exe[1],exe[2],exe[3],exe[4])
        my_db.close()
        return exercises

    def get_user_data(self, user_name):
        # User data for user with given name
        # Connect to DB, if connection fails, return empty list
        my_db = self.connect_to_DB()
        if not my_db:
            return []
        # If connection is successful run mysql query
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT email FROM users \
                                 WHERE name = '{user_name}'")
        email = mycursor.fetchall()[0]
        return [email]

    def get_workouts(self, user_name):
        # Get workouts data from DB for user
        workouts = {}
        # Connect to DB, if connection fails, return empty dict
        my_db = self.connect_to_DB()
        if not my_db:
            return workouts
        # If connection is successful run mysql query
        # Get workout data from DB
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT work_users.name, exercises.name, work_exes.order_num, work_users.extra_break_sec \
            FROM work_users \
            INNER JOIN work_exes ON work_users.work_id = work_exes.work_id \
            INNER JOIN exercises ON work_exes.exe_id = exercises.exe_id \
            WHERE work_users.user_id =(SELECT user_id FROM users WHERE name = '{user_name}');")
        wr_db = mycursor.fetchall()
        # Create Workout objects in workouts dict
        for w in wr_db:
            if w[0] in workouts:
                workouts[w[0]].exercises.append((w[1],w[2]))
                workouts[w[0]].extra_break_sec=w[3]
            else:
                workouts[w[0]]=Workout(w[0],[(w[1],w[2])],w[3])
        my_db.close()
        for key in workouts.keys():
            workouts[key].exercises.sort(key=lambda x:x[1])
        return workouts

    def delete_exercise(self,user_name,exe_name):
        # delete exercise from DB
        error = ''
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return False, error
        mycursor = my_db.cursor()
        res = False
        # Check if exercise with given name exists in database
        mycursor.execute(f"SELECT * FROM exercises \
                         WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}') AND name='{exe_name}'")
        exe = mycursor.fetchall()
        # return error message if exercise is not found
        if len(exe) == 0:
            return False, 'Exercise not found.'
        # If exercise exists - delete from database, if query fails return False and error message
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

    def delete_user(self, user_name):
        # delete current user
        error = ''
        my_db = self.connect_to_DB()
        if not my_db:
            return False, error
        mycursor = my_db.cursor()
        res = False
        mycursor.execute(f"SELECT * FROM users \
                         WHERE name = '{user_name}'")
        user = mycursor.fetchall()
        # return if no user with this name found
        if len(user) == 0:
            return False, 'User not found.'
        try:
            mycursor.execute(f"DELETE FROM users  \
                             WHERE name = '{user_name}'")
            my_db.commit()
        except mysql.connector.Error as err:
            error = err
        else:
            res = True
        my_db.close()
        return res, error

    def add_workout(self, user_name: str, workout_name: str, exercises: list, extra_break_sec: int):
        # add or update existing workout in DB, clear existing exercises in work_exe table to preserve order nums
        my_db = self.connect_to_DB()
        if not my_db:
            return False, 'DB connection error.'
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT * FROM users \
                          WHERE name = '{user_name}'")
        user = mycursor.fetchall()
        user_id = user[0][0]
        # return if no user with this name found
        if len(user) == 0:
            return False, 'User not found.'
        # add workout into work_users table
        try:
            mycursor.execute(f"INSERT INTO work_users (user_id, name, extra_break_sec) \
            VALUES ({user_id},'{workout_name}',{extra_break_sec}) ON DUPLICATE KEY UPDATE work_id = work_id ")
        except mysql.connector.Error as err:
            print(err)
            return False, 'Failed to create workout.'
        # get added workout id
        my_db.commit()
        mycursor.execute(f"SELECT work_id FROM work_users WHERE name = '{workout_name}' AND user_id = '{user_id}'")
        work_id = mycursor.fetchall()[0][0]
        # clear work exe_table
        mycursor.execute(f"DELETE FROM work_exes WHERE work_id ='{work_id}'")
        my_db.commit()
        # add exercises into work_exes table
        for i, exe_name in enumerate(exercises, 1):
            try:
                mycursor.execute(f"INSERT INTO work_exes \
                VALUES((SELECT work_id FROM work_users WHERE user_id = {user_id} AND name = '{workout_name}'),\
                (SELECT exe_id FROM exercises WHERE user_id = {user_id} AND name = '{exe_name}'),{i})\
                ON DUPLICATE KEY UPDATE work_id = work_id")
            except mysql.connector.Error as err:
                print(err)
                return False, 'Failed to add exercise.'
        my_db.commit()
        my_db.close()

    def add_user(self, user_name: str, email: str, password: str):
        # create new user in database
        if len(user_name) == 0 or len(email) == 0 or len(password) == 0:
            return False, 'Wrong input data.'
        # connect to DB, if not possible return error
        my_db = self.connect_to_DB()
        if not my_db:
            return False, 'DB connection error.'
        # if connection is ok, check if user with given name already exists
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT * FROM users \
                          WHERE name = '{user_name}'")
        user = mycursor.fetchall()
        # return error if no user with this name found
        if len(user) == 1:
            return False, 'User with that name already exists.'
        # if name is not taken -> add user
        mycursor.execute(f"INSERT INTO users (name, email, password) VALUES('{user_name}','{email}','{password}')")
        my_db.commit()
        my_db.close()
        return True, ''

    def edit_user(self, user_name, email, password):
        # edit already existing user with given data
        # connect to DB, if not possible return error
        my_db = self.connect_to_DB()
        if not my_db:
            return False, 'DB connection error.'
        mycursor = my_db.cursor()
        mycursor.execute(f"SELECT * FROM users \
                                 WHERE name = '{user_name}'")
        user = mycursor.fetchall()
        # return if no user with this name found
        if len(user) == 0:
            return False, 'User not found.'
        mycursor.execute(f"UPDATE users SET email = '{email}', password ='{password}' WHERE name = '{user_name}'")
        my_db.commit()
        my_db.close()
        return True, ''



