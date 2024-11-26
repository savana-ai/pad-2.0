from dataclasses import dataclass
import uuid
from typing import List, Dict, Optional
from domain.value_objects.artifact_type import ArtifactType
from domain.value_objects.prompt_template import PromptTemplate
from domain.value_objects.prompt import Prompt
from infrastructure.repositories.stores import prompt_store

@dataclass
class Artifact:
    id: str
    type: ArtifactType
    content_store: object = None

    def __init__(self, type: ArtifactType, content_store=None):
        """
        Initialize an Artifact instance
        
        Args:
            type (ArtifactType): Type of the artifact
            content_store (object, optional): Content storage mechanism
        """
        self.id = str(uuid.uuid4())
        self.type = type
        self.content_store = content_store

    @classmethod
    def get_prompts(cls, artifact_type: Optional[ArtifactType] = None) -> List[Dict]:
        """
        Retrieve prompts for a specific artifact type
        
        Args:
            artifact_type (Optional[ArtifactType]): Type of artifact to retrieve prompts for
        
        Returns:
            List of prompt dictionaries
        """
        # If no artifact type is provided, use the instance's type
        criteria = {
            'type': artifact_type.value if artifact_type else None
        }
        return prompt_store.find_by(criteria)

    def create_prompt(self, template: PromptTemplate, contexts: List[Dict]) -> List[Prompt]:
        """
        Create prompts based on a given template and contexts
        
        Args:
            template (PromptTemplate): Template to create prompts from
            contexts (List[Dict]): Contexts to use for prompt generation
        
        Returns:
            List of created Prompt objects
        """
        prompts = []
        template_dict = template.__dict__.copy()
        
        # Remove objects field if it exists
        template_dict.pop('objects', None)
        
        for context_item in contexts:
            prompt = Prompt(
                template=template_dict,
                context=context_item
            )
            prompts.append(prompt)
        
        return prompts