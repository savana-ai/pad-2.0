from abc import ABC, abstractmethod
from typing import Any, List, Optional

class BaseRepository(ABC):
    """
    Abstract base class defining the interface for a generic repository.
    
    This class provides a standard interface for data persistence operations
    that can be implemented by specific repository classes.
    """
    
    @abstractmethod
    def save(self, data: Any) -> Any:
        """
        Save a new item or update an existing item in the repository.
        
        Args:
            data: The data to be saved
        
        Returns:
            The saved or updated item, potentially with an assigned identifier
        """
        pass
    
    @abstractmethod
    def load(self, identifier: Any) -> Optional[Any]:
        """
        Load a specific item from the repository by its identifier.
        
        Args:
            identifier: Unique identifier for the item to be retrieved
        
        Returns:
            The retrieved item, or None if not found
        """
        pass
    
    @abstractmethod
    def delete(self, identifier: Any) -> bool:
        """
        Delete an item from the repository.
        
        Args:
            identifier: Unique identifier for the item to be deleted
        
        Returns:
            True if deletion was successful, False otherwise
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Any]:
        """
        Retrieve all items from the repository.
        
        Returns:
            A list of all items in the repository
        """
        pass
    
    @abstractmethod
    def find_by(self, criteria: dict) -> List[Any]:
        """
        Find items in the repository matching specific criteria.
        
        Args:
            criteria: A dictionary of search criteria 
        
        Returns:
            A list of items matching the given criteria
        """
        pass