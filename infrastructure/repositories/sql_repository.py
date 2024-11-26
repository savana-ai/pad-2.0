import sqlite3
from typing import Any, List, Dict, Optional
from base_repository import BaseRepository

class SQLRepository(BaseRepository):
    """
    A SQLite implementation of the BaseRepository abstract class.
    
    Provides generic database operations for SQLite databases.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the SQLite repository with a database connection.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
    
    def save(self, data: Dict[str, Any]) -> Optional[Any]:
        """
        Save data to a specified table.
        
        Args:
            data (dict): A dictionary containing:
                - 'table': Name of the table
                - 'values': Dictionary of column names and values to insert
        
        Returns:
            The row ID of the inserted record, or None
        """
        table = data.get('table')
        columns = ', '.join(data['values'].keys())
        placeholders = ', '.join(['?'] * len(data['values']))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, tuple(data['values'].values()))
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return None
    
    def load(self, identifier: Dict[str, Any]) -> Optional[tuple]:
        """
        Load a record by a specific identifier.
        
        Args:
            identifier (dict): A dictionary containing:
                - 'table': Name of the table
                - 'key': Column to search by
                - 'value': Value to match
        
        Returns:
            A tuple representing the found record, or None
        """
        table = identifier['table']
        key = identifier['key']
        value = identifier['value']
        query = f"SELECT * FROM {table} WHERE {key} = ?"
        
        try:
            self.cursor.execute(query, (value,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return None
    
    def delete(self, identifier: Dict[str, Any]) -> bool:
        """
        Delete a record by a specific identifier.
        
        Args:
            identifier (dict): A dictionary containing:
                - 'table': Name of the table
                - 'key': Column to search by
                - 'value': Value to match
        
        Returns:
            True if deletion was successful, False otherwise
        """
        table = identifier['table']
        key = identifier['key']
        value = identifier['value']
        query = f"DELETE FROM {table} WHERE {key} = ?"
        
        try:
            self.cursor.execute(query, (value,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return False
    
    def get_all(self, table: str) -> List[tuple]:
        """
        Fetch all records from a specified table.
        
        Args:
            table (str): Name of the table to fetch records from
        
        Returns:
            A list of tuples representing all records in the table
        """
        query = f"SELECT * FROM {table}"
        
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
    
    def find_by(self, criteria: Dict[str, Any]) -> List[tuple]:
        """
        Find records matching specific criteria.
        
        Args:
            criteria (dict): A dictionary containing:
                - 'table': Name of the table
                - 'conditions': Dictionary of column names and values to match
        
        Returns:
            A list of tuples matching the given criteria
        """
        table = criteria['table']
        conditions = criteria['conditions']
        where_clause = " AND ".join([f"{k} = ?" for k in conditions])
        query = f"SELECT * FROM {table} WHERE {where_clause}"
        
        try:
            self.cursor.execute(query, tuple(conditions.values()))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
    
    def __del__(self):
        """
        Ensure the database connection is closed when the object is deleted.
        """
        if hasattr(self, 'connection'):
            self.connection.close()