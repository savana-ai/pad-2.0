from dataclasses import dataclass
import uuid
from typing import Dict, Optional, List
from infrastructure.repositories.json_repository import JSONRepository
from infrastructure.repositories.stores import create_content_store
from domain.value_objects.artifact_type import ArtifactType

@dataclass
class Project:
    id: str
    name: str
    description: str
    content_store: JSONRepository

    def __init__(self, name: str, description: str = ""):
        """
        Initialize a Project instance
        
        Args:
            name (str): Name of the project
            description (str, optional): Description of the project
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.content_store = create_content_store(name)

    def initialize_with_questionnaire(self, questionnaire_content: Dict) -> None:
        """
        Initializes project with questionnaire content
        
        Args:
            questionnaire_content (Dict): The completed questionnaire
        """
        result = self.content_store.save({
            'id': ArtifactType.QUESTIONNAIRE.value,
            'type': ArtifactType.QUESTIONNAIRE.value,
            'content': [questionnaire_content]
        })

    def get_content(self, artifact_type: ArtifactType) -> Optional[List[Dict]]:
        """
        Get content for a specific artifact type
        
        Args:
            artifact_type (ArtifactType): Type of artifact to retrieve
        
        Returns:
            Optional list of content for the specified artifact type
        """
        result = self.content_store.load(artifact_type.value)
        return result.get('content') if result else None

    def update_content(self, content: List[Dict], artifact_type: ArtifactType) -> None:
        """
        Updates artifact content in storage
        
        Args:
            content (List[Dict]): New content list to store
            artifact_type (ArtifactType): Type of artifact being updated
        """
        self.content_store.save({
            'id': artifact_type.value,
            'type': artifact_type.value,
            'content': content
        })