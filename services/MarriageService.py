import sqlite3

from resources.Resources import Resources

class MarriageService:

    def __init__(self):

        with sqlite3.connect(Resources.database) as db:
            cursor = db.cursor()
            statement = 'CREATE TABLE IF NOT EXISTS marriages(' +\
                \
                'id INTEGER PRIMARY KEY AUTOINCREMENT,' +\
                'he_id INTEGER,' +\
                'she_id INTEGER,' +\
                'status VARCHAR(30),' +\
                'marital_status TEXT,' +\
                'strength INTEGER,' +\
                'first_meeting INTEGER);'
            cursor.execute(statement)
            db.commit()
    


    def __insert_data(self, id, column, data):
        try:
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()

            cursor.execute("SELECT id FROM marriages WHERE id = ?", [id])

            s = cursor.fetchone()

            if s is None:
                cursor.execute(f'INSERT INTO marriages(id, {column}) VALUES(?, ?)', [id, data])
                print(f"Marriage with id {id} created")

            db.commit()

        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()



    def __update_data(self, id, column, data):
        try:

            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute("SELECT id FROM marriages WHERE id = ?", [int(id)])

            s = cursor.fetchone()

            if s is None:
                print('Marriage with id ' + str(id) + ' not found')  
            else:
                cursor.execute(f'UPDATE marriages SET {column} = ? WHERE id = ?', [data, id])
            
            db.commit()
        except sqlite3.Error as e:
            print('Error: ', e)
        finally:
            cursor.close()
            db.close()
    


    def __getDataById(seld, nameCoumn, id):
        try:
            
            db = sqlite3.connect(Resources.database)
            cursor = db.cursor()
            cursor.execute(f"SELECT {nameCoumn} FROM marriages WHERE id = {id};")

            res = cursor.fetchone()

            db.commit()

            if res is None:
                print('Marriage with id ' + str(id) + ' not found.')  
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
            cursor.execute("SELECT id FROM marriages WHERE id = ?", [int(id)])
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
