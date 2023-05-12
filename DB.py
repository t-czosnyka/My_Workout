import string
import mysql.connector
from User import User
from Exercise import Exercise
from Workout import Workout
import hashlib
import random
import logging
from logging.handlers import RotatingFileHandler
import inspect

# Logging configuration
# create logger
logger = logging.getLogger(__name__)
# set logging level
logger.setLevel(logging.INFO)

# create formatter - time - logger_name - level - message; timer format year-month-day hour-minute-second
formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s', "%Y-%m-%d %H:%M:%S")

# create logging file handler
file_handler = RotatingFileHandler('database.log', maxBytes=2000, backupCount=5)
file_handler.setFormatter(formatter)

# add file handler to the logger
logger.addHandler(file_handler)


class DB:
    # DB class handles database operations using mysql connector
    def __init__(self):
        self.error = False
        self.error_msg = ''

        # Connect to my_workout_db, if connection fails end function
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return

        mycursor = my_db.cursor()
        # Create users table if it doesn't exist
        # Users table contain user data and login data, stored as password hash + salt
        sql = "CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY,\
                               name VARCHAR(40), email VARCHAR(40), password_hash VARCHAR(64), salt VARCHAR(64),\
                             UNIQUE(name))"
        result, self.error_msg = self.execute_sql(sql, mycursor, my_db, True)
        if not result:
            self.error = True
            return

        # Create exercises table if it doesn't exist
        # Exercise table contains exercises data with reference to user_id who owns given exercise
        sql = "CREATE TABLE IF NOT EXISTS exercises (exe_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                              name VARCHAR(40), time_work INT, time_rest INT, num_rounds INT, delay INT,\
                              UNIQUE(user_id,name), FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)"
        result, self.error_msg = self.execute_sql(sql, mycursor, my_db, True)
        if not result:
            self.error = True
            return

        # Create work_users table if it doesn't exist
        # Work users table contains workouts of every user, each workout references user_id of its owner
        # Workout data contains a name and length of extra break between exercises
        sql = "CREATE TABLE IF NOT EXISTS work_users (work_id INT AUTO_INCREMENT PRIMARY KEY, user_id INT,\
                              name  VARCHAR(40), extra_break_sec INT DEFAULT 0, UNIQUE(user_id,name),\
                              FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE)"
        result, self.error_msg = self.execute_sql(sql, mycursor, my_db, True)
        if not result:
            self.error = True
            return

        # Create work_exes table if it doesn't exist
        # each row in work_exes table represents an exercise that is part of a workout
        # it references workout that its part of from work_users table, type of exercise from exercise table
        # and ordinal number in each workout, Work_id and order number are primary key
        sql = "CREATE TABLE IF NOT EXISTS work_exes (work_id INT, exe_id INT NOT NULL, order_num INT, \
                             FOREIGN KEY (work_id) REFERENCES work_users(work_id) ON DELETE CASCADE,\
                             FOREIGN KEY (exe_id) REFERENCES exercises(exe_id) ON DELETE CASCADE,\
                             PRIMARY KEY(work_id, order_num))"
        result, self.error_msg = self.execute_sql(sql, mycursor, my_db, True)
        if not result:
            self.error = True
            return

        # Close db connection
        my_db.close()

        # # Create test users
        # self.add_user('test', 'test@test.com', 't1234')
        # self.add_user('test2', 'test@test.com', '1234')
        # # Create test exercises
        # self.save_exercise('test', 'test_exe', 10, 5, 2, 5)
        # self.save_exercise('test', 'test_exe2', 9, 4, 1, 4)
        # self.save_exercise('test', 'no_work', 20, 10, 5, 5)
        # self.save_exercise('test2', 'test2_exe', 8, 4, 1, 3)
        # self.save_exercise('test2', 'test2_exe2', 6, 2, 2, 2)
        # # Create test workout
        # self.save_workout('test', 'test_workout', ['test_exe', 'test_exe2'], 0)
        # self.save_workout('test', 'test2_workout', ['test_exe2', 'test_exe'], 5)
        # self.save_workout('test2', 'test2_workout', ['test2_exe', 'test2_exe2'], 10)

    def connect_to_DB(self):
        # connecting to remote database, return connection object if successful, return None if error occurred
        try:
            # my_db = mysql.connector.connect(
            #     host="sql.freedb.tech",
            #     user="freedb_my_workout_user",
            #     passwd="Ne8KzVs&2MFsC?r",
            #     database="freedb_my_workout_db",
            #     port=3306
            # )
            my_db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Batman123",
                database="my_workout_db"
            )
        except mysql.connector.Error as err:
            self.error = True
            self.error_msg = "DB Connection error: " + err.msg
            # log error
            logger.error(
                f"Error while connecting to DB, message: {err.msg}'")
            return None, self.error_msg
        else:
            return my_db, ''

    @staticmethod
    def execute_sql(sql: str, mycursor, my_db, commit: bool):
        # function to execute mysql statement with error handling and message logging
        # returns True if operation was successful or False and error message if error occurred
        result = False
        error = ''
        try:
            # Execute statement
            mycursor.execute(sql)
            if commit:
                # Commit changes
                my_db.commit()
        except mysql.connector.Error as err:
            # if error occurred save error message
            error = err.msg
            # log error
            # get calling function name
            calling_function = inspect.stack()[1].function
            # log error
            logger.error(
                f"Error while executing statement: '{sql}', Function: '{calling_function}, message: {error}'")
        else:
            # No error
            result = True
        return result, error

    def validate_user(self, in_login, in_password):
        # validate login and password, return True if login and password hash match database
        valid = False
        # Connect to DB, if connection fails, return False
        my_db, error = self.connect_to_DB()
        if not my_db:
            return valid, error
        mycursor = my_db.cursor()
        # look for inserted login in user table
        sql = f"SELECT name FROM users WHERE name = '{in_login}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            login = mycursor.fetchall()
            if not(len(login) == 1 and login[0][0] == in_login):
                # login was not found, log warning and return error
                # log warning
                logger.warning(f"User {in_login} not found.")
                return valid, f"User {in_login} not found."
        # compare password if login is found
        # get saved password hash and salt from DB
        sql = f"SELECT password_hash, salt FROM users WHERE name = '{in_login}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            user_pass = mycursor.fetchall()
            saved_password_hash = user_pass[0][0]
            salt = user_pass[0][1]
            # generate hash of salt from DB + inserted password
            input_password_hash = self.generate_hash_password_with_salt(in_password, salt)
            # compare saved password hash with hash generated with input password
            if saved_password_hash == input_password_hash:
                valid = True
                # log information on successful log in
                logger.info(f"User {in_login} logged in.")
            else:
                # log warning on unsuccessful log in
                logger.warning(f"Wrong password for user {in_login}.")
                error = "Wrong password."
        # Close db connection
        my_db.close()
        return valid, error

    def get_user(self, user_name):
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

    def get_exercises(self, user_name):
        # Get exercises data from DB for given user, return dict of exercises
        exercises = {}
        result = False
        # Connect to DB, if connection fails, return empty dict
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, exercises, error_msg
        # If connection is successful run mysql statement
        mycursor = my_db.cursor()
        sql = f"SELECT name,time_work,time_rest,num_rounds,delay FROM exercises \
                                WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
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
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, email, error_msg
        # If connection is successful run mysql statement
        mycursor = my_db.cursor()
        sql = f"SELECT email FROM users \
                                 WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
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
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, workouts, error_msg
        # If connection is successful run mysql statement
        # Get workout data from DB - row for each exercise in work_exes for current user
        # Data: (workout name, exercise name, exercise order number(from 1), extra break in seconds)
        mycursor = my_db.cursor()
        sql = f"SELECT work_users.name, exercises.name, work_exes.order_num, work_users.extra_break_sec \
            FROM work_users \
            INNER JOIN work_exes ON work_users.work_id = work_exes.work_id \
            INNER JOIN exercises ON work_exes.exe_id = exercises.exe_id \
            WHERE work_users.user_id =(SELECT user_id FROM users WHERE name = '{user_name}');"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            workout_data = mycursor.fetchall()
            # create workout objects
            for w in workout_data:
                workout_name, exercise_name, exercise_order_num, extra_break_sec = w[0], w[1], w[2], w[3]
                # if workout doesn't exist create new workout object
                if workout_name not in workouts:
                    workouts[workout_name] = Workout(workout_name, [], extra_break_sec)
                # add exercise to workout
                # check if current exercise order number is bigger then exercises list length
                len_difference = exercise_order_num - len(workouts[workout_name].exercises)
                if len_difference > 0:
                    # extend the list
                    workouts[workout_name].exercises.extend(['']*len_difference)
                # write exercise name in place by its order number
                workouts[workout_name].exercises[exercise_order_num-1] = exercise_name
        # Close DB connection
        my_db.close()
        return result, workouts, error

    def save_exercise(self, user_name, exe_name, worktime_sec, breaktime_sec, num_rounds, delay_sec):
        # save given exercise data into database
        # Connect to DB, if connection fails, return False
        result = False
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        # If connection is successful execute statement
        mycursor = my_db.cursor()
        # Insert exercise data into exercises table
        sql = f"INSERT INTO exercises (user_id, name,time_work,time_rest,num_rounds,delay) \
                             VALUES((SELECT user_id FROM users WHERE name='{user_name}'),\
                             '{exe_name}',{worktime_sec},{breaktime_sec},{num_rounds},{delay_sec})\
                             ON DUPLICATE KEY UPDATE time_work={worktime_sec},time_rest={breaktime_sec},\
                             num_rounds={num_rounds},delay={delay_sec}"
        result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log information about new exercise
        if result:
            logger.info(f"User {user_name} saved exercise {exe_name}.")
        # Close db connection
        my_db.close()
        return result, error

    def delete_exercise(self, user_name, exe_name):
        # delete exercise from DB
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        mycursor = my_db.cursor()
        # Check if exercise with given name exists in database
        sql = f"SELECT * FROM exercises \
                         WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}') AND name='{exe_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            exe = mycursor.fetchall()
            # return error message if exercise is not found
            if len(exe) == 0:
                result = False
                error = 'Exercise not found.'
                logger.warning(f"Exercise {exe_name}, user:{user_name} not found for deleting.")
        # If exercise exists - delete from database, if statement fails return False and error message
        if result:
            sql = f"DELETE FROM exercises WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')" \
                  f" AND name='{exe_name}'"
            result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log information about deleted exercise
        if result:
            logger.info(f"User {user_name} deleted exercise {exe_name}.")
        # Close DB connection
        my_db.close()
        return result, error

    def save_user(self, user_name: str, email: str, password: str):
        # create new user in database
        result = False
        if len(user_name) == 0 or len(email) == 0 or len(password) == 0:
            return result, 'Wrong input data.'
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        # if connection is ok, check if user with inserted name or email already exists
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}' OR email = '{email}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            user = mycursor.fetchall()
            # return error if user with this name of email already exists
            if len(user) >= 1:
                result = False
                error = 'User with that name or email already exists.'
                # Log warning
                logger.warning(f"User with name {user_name} or email {email} already exists.")
        # if name is not taken -> add user
        if result:
            # hash password
            password_hash, salt = self.generate_new_hash_password(password)
            # save user_name, email, password_hash and salt into DB
            sql = f"INSERT INTO users (name, email, password_hash, salt) \
               VALUES('{user_name}','{email}','{password_hash}','{salt}')"
            result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log information if user was successfully created
        if result:
            logger.info(f"User {user_name} successfully created.")
        # Close db connection
        my_db.close()
        return result, error

    def edit_user(self, user_name, email, password):
        # edit already existing user with given data
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            user = mycursor.fetchall()
            # return if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
                logger.warning(f"User {user_name} not found for edit.")
        if result:
            # check if inserted email address is not used by other user
            sql = f"SELECT name, email FROM users WHERE email = '{email}' AND name != '{user_name}'"
            result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            email = mycursor.fetchall()
            # return error if this email already exists in database
            if len(email) > 0:
                result = False
                error = 'Email already taken.'
                logger.warning(f"User {user_name} tried using existing email address")
        # if user is found generate password hash and salt for new password
        if result:
            password_hash, salt = self.generate_new_hash_password(password)
            # update data in DB if error occurs return False + error message
            sql = f"UPDATE users SET email = '{email}', password_hash = '{password_hash}', salt = '{salt}'\
                                  WHERE name = '{user_name}'"
            result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log information about data edit
        if result:
            logger.info(f"User {user_name} data edited.")
        # Close db connection
        my_db.close()
        return result, error

    def delete_user(self, user_name):
        # delete current user
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        # find user with given name in DB
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            user = mycursor.fetchall()
            # return False + error message if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
                logger.warning(f"User:{user_name} not found for deleting.")
        # if user is found execute delete statement
        if result:
            sql = f"DELETE FROM users WHERE name = '{user_name}'"
            result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log information about deleted user
        if result:
            logger.info(f"User {user_name} deleted.")
        # Close db connection
        my_db.close()
        return result, error

    def save_workout(self, user_name: str, workout_name: str, exercises: list, extra_break_sec: int):
        # add or update existing workout in DB, clear existing exercises in work_exe table to preserve order nums
        result = False
        user_id = 0
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg

        # Check if user with given name exists and get user_id
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM users WHERE name = '{user_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            user = mycursor.fetchall()
            # return if no user with this name found
            if len(user) == 0:
                result = False
                error = 'User not found.'
                logger.warning(f"User:{user_name} not found while saving workout.")
            else:
                user_id = user[0][0]

        # add workout into work_users table, if error occurs return false and error message
        if result:
            sql = f"INSERT INTO work_users (user_id, name, extra_break_sec) \
            VALUES ({user_id},'{workout_name}',{extra_break_sec})\
            ON DUPLICATE KEY UPDATE extra_break_sec = {extra_break_sec} "
            result, error = self.execute_sql(sql, mycursor, my_db, True)

        # get added recently added workout id
        if result:
            sql = f"SELECT work_id FROM work_users WHERE name = '{workout_name}' AND user_id = '{user_id}'"
            result, error = self.execute_sql(sql, mycursor, my_db, False)

        # clear work exe_table to preserve correct order
        if result:
            work_id = mycursor.fetchall()[0][0]
            sql = f"DELETE FROM work_exes WHERE work_id ='{work_id}'"
            result, error = self.execute_sql(sql, mycursor, my_db, True)

        # add exercises names and exercise order numbers - starting from 1, into work_exes table,
        # if error occurs return false and error message
        if result:
            for order_num, exe_name in enumerate(exercises, 1):
                # get exercise id
                sql = f"SELECT exe_id FROM exercises WHERE user_id = {user_id} AND name = '{exe_name}'"
                result, error = self.execute_sql(sql, mycursor, my_db, False)
                exe_id = mycursor.fetchall()
                if not result:
                    return result, error
                # if exercise not found in DB return and log error
                if len(exe_id) == 0:
                    logger.error(f"Error exercise {exe_name} not found in DB while saving workout.")
                    return False, f"Exercise {exe_name} not found."
                # add exercise into workout table
                sql = f"INSERT INTO work_exes \
                    VALUES((SELECT work_id FROM work_users WHERE user_id = {user_id} AND name = '{workout_name}'),\
                    {exe_id[0][0]},{order_num}) ON DUPLICATE KEY UPDATE work_id = work_id"
                result, error = self.execute_sql(sql, mycursor, my_db, True)
                if not result:
                    break
        # Log info if workout was successfully added
        if result:
            logger.info(f"Workout {workout_name} successfully saved by user {user_name}.")
        # Close db connection
        my_db.close()
        return result, error

    def delete_workout(self, user_name, workout_name):
        # delete workout from DB
        result = False
        # Connect to DB, if connection fails return False + error message
        my_db, error_msg = self.connect_to_DB()
        if not my_db:
            return result, error_msg
        # Check if workout with given name exists in database
        mycursor = my_db.cursor()
        sql = f"SELECT * FROM work_users WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')\
                          AND name='{workout_name}'"
        result, error = self.execute_sql(sql, mycursor, my_db, False)
        if result:
            workouts = mycursor.fetchall()
            # return error message if workout is not found log info
            if len(workouts) == 0:
                result = False
                error = 'Workout not found.'
                logger.warning(f"Workout {workout_name} not found in user {user_name} data.")
        # If workout exists - delete from database, if query fails return False and error message
        if result:
            sql = f"DELETE FROM work_users WHERE user_id = (SELECT user_id FROM users WHERE name='{user_name}')\
                              AND name='{workout_name}'"
            result, error = self.execute_sql(sql, mycursor, my_db, True)
        # Log info if workout successfully deleted
        if result:
            logger.info(f"Workout {workout_name} deleted by user {user_name}.")
        # Close db connection
        my_db.close()
        return result, error

    @staticmethod
    def generate_new_hash_password(password: str):
        # generate hash of given password using SHA-256 from hashlib, generate new salt
        # generate random 16 char salt
        salt = ''.join(random.choices(string.ascii_letters+string.digits, k=16))
        # create salt+password hash using SHA-256 hashing function
        password_hash = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
        return password_hash, salt

    @staticmethod
    def generate_hash_password_with_salt(password: str, salt: str):
        # generate hash from password with given salt
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest()
