from dataclasses import dataclass
from typing import List, Dict, Optional
import uuid

from domain.value_objects.artifact_type import ArtifactType
from domain.value_objects.prompt_template import PromptTemplate
from domain.value_objects.prompt import Prompt
from infrastructure.repositories.stores import prompt_store

@dataclass
class Artifact:
    id: str
    project_id: str
    type: ArtifactType
    content_store: object

    def __init__(self, project_id: str, type: ArtifactType, content_store=None):
        self.id = str(uuid.uuid4())
        self.project_id = project_id
        self.type = type
        self.content_store = content_store

    def create_prompt(self, template: PromptTemplate) -> List[Prompt]:
        """
        Create prompts based on a given template and contexts.
        
        Args:
            template (PromptTemplate): Template to create prompts from
        
        Returns:
            List of created Prompt objects
        """
        # Implement context retrieval logic here
        contexts = self._get_context(template)

        prompts = []
        template_dict = template.__dict__.copy()
        del template_dict['objects']  # Remove objects field

        for context_item in contexts:
            prompt = Prompt(
                template=template_dict,
                context=context_item
            )
            prompts.append(prompt)

        return prompts

    def _get_context(self, template: PromptTemplate) -> List[Dict]:
        """
        Get context for creating prompts.
        
        Args:
            template (PromptTemplate): Template to retrieve context for
        
        Returns:
            List of context dictionaries
        """
        # This is a placeholder. You'll need to implement actual context retrieval
        # based on your specific requirements
        return template.objects or []

    def update_content(self, content: List[Dict]) -> None:
        """
        Updates artifact content in storage.

        Args:
            content: New content list to store
        """
        # Save the content with the artifact's type as the identifier
        result = self.content_store.save({
            'id': self.type.value,
            'type': self.type.value,
            'content': content
        })

    def get_prompts(self) -> List[Dict]:
        """
        Retrieve prompts for this artifact from the prompt store.
        
        Returns:
            List of prompt dictionaries
        """
        # Find prompts related to this artifact
        criteria = {
            'artifact_id': self.id,
            'project_id': self.project_id
        }
        return prompt_store.find_by(criteria)