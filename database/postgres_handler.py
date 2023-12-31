import psycopg2
from psycopg2 import Error

class PostgresHandler:
    def __init__(self, username: str, password: str, host_name: str, port: int, database: str):
        db_params = {
            "dbname": database,
            "user": username,
            "password": password,
            "host": host_name,
            "port": port
        }
        self._connection = psycopg2.connect(**db_params)
        print("Handler Success")
    

    def create_table(self, name: str, column: str):
        cursor = self._connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({column})")
        self._connection.commit()
        cursor.close()
    
    def check_row_exists(self, table_name: str, column_name: str, value: str):
        cursor = self._connection.cursor()
        query = f"SELECT 1 FROM {table_name} WHERE {column_name} = %s"
        cursor.execute(query, (value,))
        result = cursor.fetchone()
        cursor.close()

        if result is not None:
            return True
        else:
            return False
    
    def insert_row(self, table_name, column, data):
        try:
            cursor  = self._connection.cursor()
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({column}) VALUES ({placeholders})"
            cursor.execute(query, data)
            self._connection.commit()
            print("Data Inserted:", data)
        except Error as err:
            self._connection.rollback()
            print("Error inserting data")
            print(err)
            if "duplicate key" not in str(err).lower():
                return False
        return True
    
    def get_rows(self, table_name: str, column: str, value: str):
        try:
            cursor = self._connection.cursor()
            query = f"SELECT * FROM {table_name} WHERE {column} = %s"
            cursor.execute(query, (value,))
            result = cursor.fetchall()
            return result
        except Error as e:
            self._connection.rollback()
            print(f"Failed to fetch row from {table_name} WHERE {column} is {value}")
            print(e)
            return False
    
    def close_connection(self):
        self._connection.close()
      
