from models.User import User
from resources.Resources import Resources
import sqlite3

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
                'job VARCHAR(30),' +\
                'age INTEGER);'
            cursor.execute(statement)
            db.commit()


    def insertData(self, id, column, data):
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
    

    def updateDataById(self, id, column, data):
        try:

            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute("SELECT id FROM users WHERE id = ?", [int(id)])

            s = cursor.fetchone()

            if s is None:
                print('User with id ' + str(id) + ' not found')  
            else:
                cursor.execute(f'UPDATE users SET {column} = ? WHERE id = ?', [data, id])
            
            db.commit()
        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()
        
    
    def getDataById(seld, id, nameColumn):
        try:
            
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute(f"SELECT {nameColumn} FROM users WHERE id = {id};")

            res = cursor.fetchone()

            db.commit()

            if res is None:
                print('User with id ' + str(id) + ' not found.')  
                return None
            else:
                return res[0]

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
                return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7])

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()


        
    def deleteUser(self, id):
        try:
            
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute(f"DELETE from users WHERE id = {id};")
            print(f"User with id {id} deleted.")
            db.commit()

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()


    
    

