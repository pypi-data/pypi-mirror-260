import json
import os

class Database:
    
    def __init__(self, path="./db/"):
        self.databases = {}  # Utiliser un dictionnaire pour stocker les bases de données
        self.path = path
        self.current_db = None  # Base de données actuellement sélectionnée
        self.query_engine = None
        self.load_databases()  # Charger les bases de données existantes lors de l'initialisation

    def load_databases(self):
        # Parcourir tous les fichiers JSON dans le répertoire spécifié
        for file_name in os.listdir(self.path):
            if file_name.endswith(".json"):
                file_path = os.path.join(self.path, file_name)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.databases[file_path] = data

    def execute_query_builder(self, query, query_builder_instance):
        query_builder_instance.execute_db_action(self, query)

    @staticmethod
    def generate_table_ascii(data, table_name):
        if not data:
            return

        # Récupérer les colonnes
        columns = list(data[0].keys())

        # Calculer la largeur de chaque colonne
        column_widths = {}
        for column in columns:
            column_widths[column] = max(len(column), max(len(str(row[column])) for row in data))

        # Calculer la largeur totale du tableau
        table_width = sum(column_widths.values()) + len(columns) * 3 + 1

        # Afficher le nom de la table centré au-dessus du tableau
        print("+" + "-" * (table_width - 2) + "+")
        print("| {} |".format(table_name.center(table_width - 4)))

        # Afficher le tableau
        print("+" + "-" * (table_width - 2) + "+")
        print("| {} |".format(" | ".join(column.center(column_widths[column]) for column in columns)))
        print("+" + "-" * (table_width - 2) + "+")
        for row in data:
            print("|", end="")
            for column in columns:
                value = str(row.get(column, ""))
                print(" {} |".format(value.ljust(column_widths[column])), end="")
            print()
        print("+" + "-" * (table_width - 2) + "+")

    def create_db(self, db_name):
        db_file = os.path.join(self.path, db_name + ".json")

        if db_file in self.databases:
            print("Database {} already exists.".format(db_name))
        else:
            self.databases[db_file] = {}  # Ajouter la base de données au dictionnaire
            self._save_db(db_file)
            print("Database {} created.".format(db_name))

    def delete_db(self, db_name):
        db_file = os.path.join(self.path, db_name + ".json")
        
        if db_file in self.databases:
            os.remove(db_file)
            del self.databases[db_file]
            print("Database {} deleted.".format(db_name))
        else:
            print("Database {} does not exist.".format(db_name))

    def show_db(self):
        print("Liste des bases de données:")
        for db_file in self.databases:
            db_name = os.path.basename(db_file).split(".json")[0]
            print(db_name)

    def select_db(self, db_name):
        db_file = os.path.join(self.path, db_name + ".json")
        
        if db_file in self.databases:
            print("Database {} selected.".format(db_name))
            self.current_db = db_file  # Sélectionner la base de données
        else:
            print("Database {} does not exist.".format(db_name))

    def create_table(self, table_name):
        if self.current_db:
            if table_name not in self.databases[self.current_db]:
                self.databases[self.current_db][table_name] = {}
                self._save_db(self.current_db)
                print("Table {} created.".format(table_name))
            else:
                print("Table {} already exists.".format(table_name))
        else:
            print("No database selected.")

    def delete_table(self, table_name):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                del self.databases[self.current_db][table_name]
                self._save_db(self.current_db)
                print("Table {} deleted.".format(table_name))
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def show_table(self):
        if self.current_db:
            print("Liste des tables:")
            for table_name in self.databases[self.current_db]:
                print(table_name)
        else:
            print("No database selected.")

    def insert(self, table_name, data):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                table = self.databases[self.current_db][table_name]
                table[len(table) + 1] = data
                self._save_db(self.current_db)
                print("Data inserted.")
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def delete_record(self, table_name, record_id):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                table = self.databases[self.current_db][table_name]
                if record_id in table:
                    del table[record_id]
                    self._save_db(self.current_db)
                    print("Record {} deleted.".format(record_id))
                else:
                    print("Record {} does not exist.".format(record_id))
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def delete_all_records(self, table_name):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                self.databases[self.current_db][table_name] = {}
                self._save_db(self.current_db)
                print("All records deleted.")
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def remove_key_from_record_by_id(self, table_name, record_id, key):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                table = self.databases[self.current_db][table_name]
                if record_id in table:
                    record = table[record_id]
                    if key in record:
                        del record[key]
                        self._save_db(self.current_db)
                        print("Key {} removed from record {}.".format(key, record_id))
                    else:
                        print("Key {} does not exist in record {}.".format(key, record_id))
                else:
                    print("Record {} does not exist.".format(record_id))
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def show_records(self, table_name):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                table = self.databases[self.current_db][table_name]
                data = []
                for record_id, record in table.items():
                    record_data = {"id": record_id}  # Créer un dictionnaire pour stocker les données de l'enregistrement
                    record_data.update(record)  # Mettre à jour le dictionnaire avec les données de l'enregistrement
                    data.append(record_data)  # Ajouter le dictionnaire à la liste des données

                self.generate_table_ascii(data, table_name)  # Afficher les données sous forme de tableau ASCII
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def show_record_by_id(self, table_name, record_id):
        if self.current_db:
            if table_name in self.databases[self.current_db]:
                table = self.databases[self.current_db][table_name]
                if record_id in table:
                    print("Record:", table[record_id])
                else:
                    print("Record {} does not exist.".format(record_id))
            else:
                print("Table {} does not exist.".format(table_name))
        else:
            print("No database selected.")

    def _save_db(self, file_path):
        with open(file_path, 'w') as f:
            json.dump(self.databases[file_path], f, indent=4)
