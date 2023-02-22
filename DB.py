import string

import mysql.connector
from User import User
from Exercise import Exercise
from Workout import Workout
import hashlib
import random
class DB:
    # DB class handles database operations using mysql connector
    def __init__(self):
        self.error = False
        self.error_msg = ''
        # Connect to mysql server
        try:
            my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Batman123"
            )
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err.msg
            return

        mycursor = my_db.cursor()
        # Create database my_workout_db if not present
        try:
            mycursor.execute("CREATE DATABASE IF NOT EXISTS my_workout_db")
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err.msg
        # Close DB connection
        my_db.close()
        # End function if error occurred
        if self.error:
            return

        # Reconnect to my_workout_db, if connection fails end function
        my_db = self.connect_to_DB()
        if not my_db:
            return

        mycursor = my_db.cursor()
        # Create tables if they dont exist
        try:
            mycursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,\
                               name VARCHAR(40), email VARCHAR(40), password_hash VARCHAR(64), salt VARCHAR(64),\
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
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err.msg
        # Commit changes and close DB connection
        my_db.commit()
        my_db.close()
        # End function if error occurred
        if self.error:
            return

        # Create test users
        self.add_user('test', 'test@test.com', 't1234')
        self.add_user('test2', 'test@test.com', '1234')
        # Create test exercises
        self.save_exercise('test', 'test_exe', 10, 5, 2, 5)
        self.save_exercise('test', 'test_exe2', 9, 4, 1, 4)
        self.save_exercise('test', 'no_work', 20, 10, 5, 5)
        self.save_exercise('test2', 'test2_exe', 8, 4, 1, 3)
        self.save_exercise('test2', 'test2_exe2', 6, 2, 2, 2)
        # Create test workout
        self.save_workout('test', 'test_workout', ['test_exe', 'test_exe2'], 0)
        self.save_workout('test', 'test2_workout', ['test_exe2', 'test_exe'], 5)
        self.save_workout('test2', 'test2_workout', ['test2_exe', 'test2_exe2'], 10)

    @staticmethod
    def execute_sql(sql: str, mycursor):
        # function to execute mysql statement, handles errors,
        # returns True if operation was successful or False and error message if error occurred
        result = False
        error = ''
        try:
            mycursor.execute(sql)
        except mysql.connector.Error as err:
            # if error occurred save error message
            error = err.msg
        else:
            # No error
            result = True
        return result, error


    def connect_to_DB(self):
        # connecting to the database, return connection object if successful, return None if error occurred
        try:
            my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Batman123",
                database="my_workout_db"
            )
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = err.msg
            return None
        else:
            return my_db

    def validate(self, in_login, in_password):
        # validate login and password, return True if login and password hash match database
        valid = False
        login_found = False
        # Connect to DB, if connection fails, return False
        my_db = self.connect_to_DB()
        if not my_db:
            return False
        mycursor = my_db.cursor()
        # get logins from DB
        mycursor.execute("SELECT name FROM users")
        logins = mycursor.fetchall()
        # compare logins with inserted login
        for login in logins:
            if login[0] == in_login:
                login_found = True
                break
        # if login is in DB compare password
        if login_found:
            # get saved password hash and salt from DB
            mycursor.execute(f"SELECT password_hash, salt FROM users WHERE name = '{in_login}'")
            user_pass = mycursor.fetchall()
            saved_password_hash = user_pass[0][0]
            salt = user_pass[0][1]
            # generate hash of inserted salt + inserted password
            input_password_hash = self.generate_hash_password_with_salt(in_password, salt)
            # compare saved password hash with hash generated with input password
            valid = saved_password_hash == input_password_hash
        my_db.close()
        return valid

    def get_user(self,user_name):
        # On successful login create and return User object with data from DB
        # Get exercises, end function and return error message if error occurred
        result, exercises, error = self.get_exercises(user_name)
        if not result:
            return None, error
        # Get workouts, end function and return error message if error occurred
        result, workouts, error = self.get_workouts(user_name)
        if not result:
            return None, error
        # Get user data, end function and return error message if error occurred
        result, data, error = self.get_user_data(user_name)
        if not result:
            return None, error
        # if all queries were successful create User class object, if not return None
        user = User(user_name, exercises, workouts, *data)
        return user, ''

    def get_exercises(self,user_name):
        # Get exercises data from DB for user
        exercises = {}
        result = False
        # Connect to DB, if connection fails, return empty dict
        my_db = self.connect_to_DB()
        if not my_db:
            return result, exercises, "DB connection error."
        # If connection is successful run mysql statement
        mycursor = my_db.cursor()
        sql = f"SELECT name,time_work,time_rest,num_rounds,delay FROM exercises \
                                WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            exes = mycursor.fetchall()
            # create Exercise class objects from fetched data
            for exe in exes:
                exercises[exe[0]] = Exercise(exe[0], exe[1], exe[2], exe[3], exe[4])
        # Close DB connection
        my_db.close()
        return result, exercises, error

    def get_user_data(self, user_name):
        # User data for user with given name
        # Connect to DB, if connection fails, return false
        email = ''
        result = False
        my_db = self.connect_to_DB()
        if not my_db:
            return result, email, "DB connection error."
        # If connection is successful run mysql statement
        mycursor = my_db.cursor()
        sql = f"SELECT email FROM users \
                                 WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            email = mycursor.fetchall()[0]
        # Close DB connection
        my_db.close()
        return result, email, error

    def get_workouts(self, user_name):
        # Get workouts data from DB for user
        workouts = {}
        result = False
        # Connect to DB, if connection fails, return empty dict
        my_db = self.connect_to_DB()
        if not my_db:
            return result, workouts, "DB connection error."
        # If connection is successful run mysql statement
        # Get workout data from DB - row for each exercise in work_exes for current user
        # Data: (workout name, exercise name, exercise order number, extra break in seconds)
        mycursor = my_db.cursor()
        sql = f"SELECT work_users.name, exercises.name, work_exes.order_num, work_users.extra_break_sec \
            FROM work_users \
            INNER JOIN work_exes ON work_users.work_id = work_exes.work_id \
            INNER JOIN exercises ON work_exes.exe_id = exercises.exe_id \
            WHERE work_users.user_id =(SELECT user_id FROM users WHERE name = '{user_name}');"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            wr_db = mycursor.fetchall()
            # Create Workout objects in workouts dict
            for w in wr_db:
                workout_name, exercise_name, exercise_order_num, extra_break_sec = w[0], w[1], w[2], w[3]
                # if workout exists add exercises
                if workout_name in workouts:
                    workouts[workout_name].exercises.append((exercise_name, exercise_order_num))
                    workouts[workout_name].extra_break_sec = extra_break_sec
                # if workout doesn't exist create new workout object
                else:
                    workouts[workout_name] = Workout(workout_name, [(exercise_name, exercise_order_num)],
                                                     extra_break_sec)
                # sort exercises in each workout by its order number
            for key in workouts.keys():
                workouts[key].exercises.sort(key=lambda x: x[1])
        # Close DB connection
        my_db.close()
        return result, workouts, error

    def save_exercise(self, user_name, exe_name, worktime_sec, breaktime_sec, num_rounds, delay_sec):
        # save given exercise data into database
        # Connect to DB, if connection fails, return False
        result = False
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        # If connection is successful execute statement
        mycursor = my_db.cursor()
        sql = f"INSERT INTO exercises (user_id, name,time_work,time_rest,num_rounds,delay) \
                             VALUES((SELECT user_id FROM users WHERE name='{user_name}'),\
                             '{exe_name}',{worktime_sec},{breaktime_sec},{num_rounds},{delay_sec})\
                             ON DUPLICATE KEY UPDATE time_work={worktime_sec},time_rest={breaktime_sec},\
                             num_rounds={num_rounds},delay={delay_sec}"
        result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def delete_exercise(self,user_name,exe_name):
        # delete exercise from DB
        error = ''
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        mycursor = my_db.cursor()
        # Check if exercise with given name exists in database
        sql = f"SELECT * FROM exercises \
                         WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}') AND name='{exe_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            exe = mycursor.fetchall()
            # return error message if exercise is not found
            if len(exe) == 0:
                result = False
                error = 'Exercise not found.'
        # If exercise exists - delete from database, if statement fails return False and error message
        if result:
            sql = f"DELETE FROM exercises WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')" \
                  f" AND name='{exe_name}'"
            result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def delete_user(self, user_name):
        # delete current user
        result = False
        error = ''
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        # find user with given name in DB
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            user = mycursor.fetchall()
            # return False + error message if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
        # if user is found execute delete statement
        if result:
            sql = f"DELETE FROM users WHERE name = '{user_name}'"
            result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def save_workout(self, user_name: str, workout_name: str, exercises: list, extra_break_sec: int):
        # add or update existing workout in DB, clear existing exercises in work_exe table to preserve order nums
        result = False
        user_id = 0
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'

        # Check if user with given name exists and get user_id
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            user = mycursor.fetchall()
            # return if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
            else:
                user_id = user[0][0]

        # add workout into work_users table, if error occurs return false and error message
        if result:
            sql = f"INSERT INTO work_users (user_id, name, extra_break_sec) \
            VALUES ({user_id},'{workout_name}',{extra_break_sec})\
            ON DUPLICATE KEY UPDATE extra_break_sec = {extra_break_sec} "
            result, error = self.execute_sql(sql, mycursor)

        # get added recently added workout id
        if result:
            my_db.commit()
            workout_added = True
            sql = f"SELECT work_id FROM work_users WHERE name = '{workout_name}' AND user_id = '{user_id}'"
            result, error = self.execute_sql(sql, mycursor)

        # clear work exe_table to preserve correct order
        if result:
            work_id = mycursor.fetchall()[0][0]
            sql = f"DELETE FROM work_exes WHERE work_id ='{work_id}'"
            result, error = self.execute_sql(sql, mycursor)

        # add exercises names and exercise order numbers - starting from 1, into work_exes table,
        # if error occurs return false and error message
        if result:
            my_db.commit()
            for order_num, exe_name in enumerate(exercises, 1):
                sql = f"INSERT INTO work_exes \
                    VALUES((SELECT work_id FROM work_users WHERE user_id = {user_id} AND name = '{workout_name}'),\
                    (SELECT exe_id FROM exercises WHERE user_id = {user_id} AND name = '{exe_name}'),{order_num})\
                    ON DUPLICATE KEY UPDATE work_id = work_id"
                result, error = self.execute_sql(sql, mycursor)
                if not result:
                    break
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def delete_workout(self, user_name, workout_name):
        # delete workout from DB
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        # Check if workout with given name exists in database
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM work_users WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')\
                          AND name='{workout_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            workouts = mycursor.fetchall()
            # return error message if exercise is not found
            if len(workouts) == 0:
                result = False
                error = 'Workout not found.'
        # If workout exists - delete from database, if query fails return False and error message
        if result:
            sql = f"DELETE FROM work_users WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')\
                              AND name='{workout_name}'"
            result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def add_user(self, user_name: str, email: str, password: str):
        # create new user in database
        result = False
        if len(user_name) == 0 or len(email) == 0 or len(password) == 0:
            return result, 'Wrong input data.'
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        # if connection is ok, check if user with given name already exists
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            user = mycursor.fetchall()
            # return error if no user with this name found
            if len(user) >= 1:
                result = False
                error = 'User with that name already exists.'
        # if name is not taken -> add user
        if result:
            # hash password
            password_hash, salt = self.generate_new_hash_password(password)
            # save user_name, email, password_hash and salt into DB
            sql = f"INSERT INTO users (name, email, password_hash, salt) \
            VALUES('{user_name}','{email}','{password_hash}','{salt}')"
            result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    def edit_user(self, user_name, email, password):
        # edit already existing user with given data
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db = self.connect_to_DB()
        if not my_db:
            return result, 'DB connection error.'
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor)
        if result:
            user = mycursor.fetchall()
            # return if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
        # if user is found generate password hash and salt for new password
        if result:
            password_hash, salt = self.generate_new_hash_password(password)
            # update data in DB if error occurs return False + error message
            sql = f"UPDATE users SET email = '{email}', password_hash = '{password_hash}', salt = '{salt}'\
                               WHERE name = '{user_name}'"
            result, error = self.execute_sql(sql, mycursor)
        # commit changes and close db connection
        my_db.commit()
        my_db.close()
        return result, error

    @staticmethod
    def generate_new_hash_password(password: str):
        # generate hash of given password using SHA-256 from hashlib, generate new salt
        # generate random 16 char salt
        salt = ''.join(random.choices(string.ascii_letters+string.digits,k=16))
        # create salt+password hash using SHA-256 hashing function
        password_hash = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        return password_hash, salt

    @staticmethod
    def generate_hash_password_with_salt(password: str, salt: str):
        # generate hash from password with given salt
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()




