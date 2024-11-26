import os
from infrastructure.repositories.json_repository import JSONRepository

def create_content_store(project_name: str):
    """
    Create a content store for a specific project.
    
    Args:
        project_name (str): Name of the project to create a content store for
    
    Returns:
        JSONRepository: A JSON repository for storing project content
    """
    # Ensure the base db directory exists
    base_db_path = os.path.join('db', project_name)
    os.makedirs(base_db_path, exist_ok=True)
    
    return JSONRepository(base_db_path)

# Global prompt store
prompt_store = JSONRepository(os.path.join('db', 'prompts'))