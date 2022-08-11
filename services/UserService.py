from models.User import User
from resources.Resources import Resources
import sqlite3
import telebot
from telebot import types

class UserService:

    def __init__(self):

        with sqlite3.connect(Resources.database) as db:
            cursor = db.cursor()
            statement = 'CREATE TABLE IF NOT EXISTS users(' +\
                \
                'id INTEGER PRIMARY KEY,' +\
                'name VARCHAR(30),' +\
                'description TEXT,' +\
                'sex VARCHAR(30),' +\
                'money INTEGER,' +\
                'marital_status TEXT,' +\
                'job VARCHAR(30));'
            cursor.execute(statement)
            db.commit()


    def __insert_data(self, id, column, data):
        try:
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()

            cursor.execute("SELECT id FROM users WHERE id = ?", [id])

            s = cursor.fetchone()

            if s is None:
                cursor.execute(f'INSERT INTO users(id, {column}) VALUES(?, ?)', [id, data])
                print(f"User with id {id} created")

            db.commit()

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()
    

    def __update_data(self, id, username, column, data):
        try:

            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", [int(id)])

            s = cursor.fetchone()

            if s is None:
                print('User with id ' + str(id) + ' not found')  
                self.__insert_data(id, "name", username)
                self.__update_data(id, username, column, data)
            else:
                cursor.execute(f'UPDATE users SET {column} = ? WHERE id = ?', [data, id])
            
            db.commit()
        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()


    def checkIfUserExistInDB(self, id):
        try:
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", [int(id)])
            s = cursor.fetchone()
            db.commit()
            
            if s is None:
                return False
            else:
                return True
            
        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()


    def getUserById(self, id):

        try:
            
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", [id])

            res = cursor.fetchone()

            db.commit()

            if res is None:
                print('User with id ' + str(id) + ' not found.')  
                return None
            else:
                return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()

    
    def addColumn(self, nameColumn, typeColumn):
        try:
            
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute(f"ALTER TABLE users ADD COLUMN {nameColumn} {typeColumn};")
            db.commit()

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()


    def createUserIfNotExist(self, id, username):
        self.__insert_data(id, "name", username)
    

    def updateNameById(self, id, username):
        self.__update_data(id, username, "name", username)


    def updateDescriptionById(self, id, username, description):
        self.__update_data(id, username, "description", description)
    

    def updateSexById(self, id, username, sex):
        self.__update_data(id, username, "sex", sex)
    

    def updateMoneyById(self, id, username, money):
        self.__update_data(id, username, "money", money)
    

    def updateMaritalStatusById(self, id, username, marital_status):
        self.__update_data(id, username, "marital_status", marital_status)
    

    def updateJobById(self, id, username, job):
        self.__update_data(id, username, "job", job)
    
    

