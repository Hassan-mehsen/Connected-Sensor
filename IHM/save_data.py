import sqlite3
import csv



""""
        This module includes the SaveData class, designed to streamline database management. It provides functionalities like data insertion, 
        retrieval, table creation, and CSV exporting. Tailored for efficient data handling, developers can effectively structure and manage information 
        within their applications using this module.

"""

class saveData():

    def __init__(self,db_name):

        try : 
            self.connexion = sqlite3.connect(db_name) 
            self.cursor = self.connexion.cursor()

        except sqlite3.Error as e : 
            print("Erreur lors de la connexion à la base de données:", e)


    # pour génraliser il faut prendre en paramètre les noms des colones et leur type
    def create_table(self):
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS SI1151 (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                    infrared_value INTEGER NOT NULL,
                                    visible_value INTEGER NOT NULL
                                )''')
            self.connexion.commit()
            print("Table SI1151 created successfully.")
        except sqlite3.Error as e:
            print("Error creating table:", e)


     #pour généraliser il faut prendre en paramètre le nom du tableau ici c'est SI1151
    def insert_data(self, column_1_name, column_2_name, value_1, value_2):

        try:
            self.cursor.execute(f'''INSERT INTO SI1151 ({column_1_name}, {column_2_name}) 
                                   VALUES (?, ?)''', (value_1, value_2))
            self.connexion.commit()
            print("Data inserted successfully.")
        except sqlite3.Error as e:
            print("Error inserting data:", e)



    def fetch_data(self):
        try:
            self.cursor.execute('''SELECT * FROM SI1151''')
            data  = self.cursor.fetchall()
            return data 
        except sqlite3.Error as e:
            print("Erreur lors de la récupération des données:", e)
            return []
        
        
    def export_to_csv(self, csv_file):

        data = self.fetch_data()
        if data:
            try:
                with open(csv_file, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Écrire les en-têtes
                    writer.writerow(['date_creation', 'infrared_value', 'visible_value'])
                    # Écrire les données
                    for row in data:
                        date = str(row[1])
                        ir = str(row[2])
                        vis= str(row[3])
                        writer.writerow([date,ir,vis])
                
                print(f"Les données ont été exportées avec succès vers {csv_file}.")
            except Exception as e:
                print(f"Erreur lors de l'exportation vers le fichier CSV: {e}")
        else:
            print("Aucune donnée à exporter.")

    def close(self):
        if self.connexion:
            self.connexion.close()


    

    
   