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

    def __init__(self, name: str, description: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.content_store = create_content_store(name)

    def initialize_with_questionnaire(self, questionnaire_content: Dict) -> None:
        """
        Initializes project with questionnaire content.
        
        Args:
            questionnaire_content: The completed questionnaire
        """
        # Store questionnaire content as a single-item list
        result = self.content_store.save({
            'id': ArtifactType.QUESTIONNAIRE.value,
            'type': ArtifactType.QUESTIONNAIRE.value,
            'content': [questionnaire_content]
        })

    def get_content(self, artifact_type: ArtifactType) -> Optional[List[Dict]]:
        """
        Get content for a specific artifact type.
        
        Args:
            artifact_type (ArtifactType): Type of artifact to retrieve
        
        Returns:
            Optional list of content for the specified artifact type
        """
        result = self.content_store.load(artifact_type.value)
        return result['content'] if result else None