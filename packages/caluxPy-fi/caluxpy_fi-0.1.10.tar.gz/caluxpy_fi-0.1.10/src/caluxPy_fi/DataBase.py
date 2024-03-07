import pymongo, pyodbc, os
import pandas as pd

#Clase Abstracta
class DataBase():
    
    def mongo_db(self):
        client = pymongo.MongoClient('mongodb+srv://luistavarez:Luimamp1@cluster0.9qjscu4.mongodb.net/')
        db = client['Calculador']
        col = db['Base_Titulos']
        raw_data = col.find()
        df = pd.DataFrame(raw_data)
        db_loaded = True
        return raw_data, df, db_loaded
    
    def ms_access_db(self, ruta):
        #ruta = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        #ruta = os.path.join(os.getcwd(), 'resources')
        archivo = 'base_titulos.accdb'
        driver = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};'
        dbq = f'DBQ={os.path.join(ruta, archivo)};'
        sql_connection = driver + dbq
        table_titulos = 'base_titulos'
        table_yields = 'rendimientos'

        conn = pyodbc.connect(sql_connection)
        
        query = f'select * from {table_titulos}'
        base_titulos = pd.read_sql(query, conn)

        query = f'select * from {table_yields}'
        base_rendimientos = pd.read_sql(query, conn)

        return base_titulos, base_rendimientos