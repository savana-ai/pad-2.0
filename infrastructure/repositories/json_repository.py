import json
import os
from typing import Any, List, Dict, Optional
from base_repository import BaseRepository

class JSONRepository(BaseRepository):
    """
    A JSON file-based implementation of the BaseRepository abstract class.
    
    Provides generic data persistence operations using JSON files in a specified directory.
    """
    
    def __init__(self, db_directory: str):
        """
        Initialize the JSON repository with a directory for storing JSON files.
        
        Args:
            db_directory (str): Path to the directory where JSON files will be stored
        """
        self.db_directory = db_directory
        os.makedirs(db_directory, exist_ok=True)
    
    def save(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Save data to a JSON file named after the item's identifier.
        
        Args:
            data (dict): The data to be saved, expected to have an 'id' key
        
        Returns:
            The identifier of the saved item, or None if saving failed
        """
        identifier = data.get('id')
        if identifier is None:
            raise ValueError("Data must include an 'id' field")
        
        try:
            file_path = os.path.join(self.db_directory, f"{identifier}.json")
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=2)
            return identifier
        except (IOError, TypeError) as e:
            print(f"Error saving data: {e}")
            return None
    
    def load(self, identifier: str) -> Optional[Dict[str, Any]]:
        """
        Load a JSON file by its identifier.
        
        Args:
            identifier (str): The unique identifier of the item to load
        
        Returns:
            The loaded data as a dictionary, or None if the file doesn't exist
        """
        file_path = os.path.join(self.db_directory, f"{identifier}.json")
        
        try:
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'r') as file:
                return json.load(file)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            return None
    
    def delete(self, identifier: str) -> bool:
        """
        Delete a JSON file by its identifier.
        
        Args:
            identifier (str): The unique identifier of the item to delete
        
        Returns:
            True if deletion was successful, False otherwise
        """
        file_path = os.path.join(self.db_directory, f"{identifier}.json")
        
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except OSError as e:
            print(f"Error deleting file: {e}")
            return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all JSON files from the directory.
        
        Returns:
            A list of all data items stored in JSON files
        """
        all_data = []
        
        try:
            all_files = os.listdir(self.db_directory)
            for file_name in all_files:
                if file_name.endswith('.json'):
                    file_path = os.path.join(self.db_directory, file_name)
                    with open(file_path, 'r') as file:
                        all_data.append(json.load(file))
            return all_data
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error retrieving all data: {e}")
            return []
    
    def find_by(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Find items matching specific criteria.
        
        Args:
            criteria (dict): A dictionary of key-value pairs to match
        
        Returns:
            A list of items matching all specified criteria
        """
        results = []
        try:
            all_data = self.get_all()
            for item in all_data:
                if all(item.get(k) == v for k, v in criteria.items()):
                    results.append(item)
            return results
        except Exception as e:
            print(f"Error finding items: {e}")
            return []