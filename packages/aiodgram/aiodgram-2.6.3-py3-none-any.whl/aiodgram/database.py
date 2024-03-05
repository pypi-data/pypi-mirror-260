import sqlite3

class Database:
    def __init__(self,
                 database_file: str = None) -> None:
        
        """
        Setting your database 

        :param database_file: str, name your database file, default None
        """
        
        if database_file == None:
            raise ValueError("Enter the database file")
        
        self.connect = sqlite3.connect(database=database_file)
        self.cursor = self.connect.cursor()

    
    
    def create_data(self,
                 table: str = None,
                 columns: list = None,
                 values: list = None):
        

        """
        Creating a cell in a database table

        :param table: str, name table in your database, default None
        :param column: list, list columns in your database, default None
        :param values: list, the data you want to enter into the columns, default None
        """
        
        c = 0
        with self.connect:
            while True:
                if c == 0:
                    c+=1
                    self.cursor.execute(f"INSERT INTO {table} ({columns[0]}) VALUES (?)", (values[0],))
                
                else:
                    for i in range(len(columns)):
                        self.edit_data(table, columns[i], values[i], search_column=columns[0], search_data=values[0])
                    
                    break

        return True
            
    


    def select_data(self,
                    table: str = None,
                    *,
                    column: str = None,
                    search_column: str = None,
                    search_data: str = None):

        """
        Return list with your datas
        
        :param table: str, name table in your database, default None
        :param column: str, name column you want to return, default None
        :param search_column: str, the name of the column you are looking for, default None
        :param search_data: str, the name of the data you are looking for, default None
        """


        with self.connect:
            if column == None:
                if search_column == None:
                    return self.cursor.execute(f"SELECT * FROM {table}").fetchall()
                
                else:
                    return self.cursor.execute(f"SELECT * FROM {table} WHERE {search_column} = ?", (search_data,)).fetchall()
            
            else:
                if search_data == None:
                    return self.cursor.execute(f"SELECT {column} FROM {table}").fetchall()
                
                else:
                    return self.cursor.execute(f"SELECT {column} FROM {table} WHERE {search_column} = ?", (search_data,)).fetchall()
        


    def edit_data(self,
                  table: str = None,
                  column: str = None,
                  new_data = None,
                  search_column: str = None,
                  search_data: str = None):

        """
        Edit data in your database
        
        :param table: str, name table in your database, default None
        :param column: str, name column you want to return, default None
        :param new_data: any, new data in cell your database, default None
        :param search_column: str, the name of the column you are looking for, default None
        :param search_data: str, the name of the data you are looking for, default None
        """
        
        with self.connect:
            return self.cursor.execute(f"UPDATE `{table}` SET `{column}` = ? WHERE {search_column} = (?)", (new_data, search_data,))
        

    def delete_data(self,
                    table: str = None,
                    search_column: str = None,
                    search_data: str = None):
        
        """
        Delete data from database

        :param table: str, name table in your database, default None
        :param search_column: str, the name of the column you are looking for, default None
        :param search_data: str, the name of the data you are looking for, default None
        """
        
        return self.cursor.execute(f"DELETE FROM {table} WHERE {search_column} = ?", (search_data,))