import mysql.connector

class Conexion():

    def __init__(self, usuario:str, contra:str):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user=usuario,
            password=contra,
            database="escuela"
            )
        self.cursor = self.mydb.cursor()

    def _showContents(self):
        print("--------------------------")
        for i in self.cursor:
            print(i)
        print("--------------------------\n")
    
    def actualizarLugares(self, lista):

        try:
            for i, l in enumerate (lista):
                    self.cursor.execute(f"INSERT IGNORE INTO lugares (id, status) VALUES ({i}, {l});")
                    print(f"ID: {i} Estado: {l} ")
        except:
            print("No se pudo pinche puta")
        finally:
            self.mydb.commit()

