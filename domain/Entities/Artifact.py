# artifact store

from dataclasses import dataclass
from typing import List, Dict
import uuid

from domain.value_objects.prompt import Prompt
from infrastructure.repositories.stores import content_store  # Use this directly

@dataclass
class Artifact:
    id: str
    project_id: str
    type: ArtifactType
    content_store: object  # Type hint as `object` if it's not a class (JSONRepository instance)

    def __init__(self, project_id: str, type: ArtifactType, content_store=content_store):
        self.id = str(uuid.uuid4())
        self.project_id = project_id
        self.type = type
        self.content_store = content_store

    def create_prompt(self, template: PromptTemplate) -> List[Prompt]:
        from application.queries.artifact_queries import get_context  # Dynamic import for queries
        contexts = get_context(self.content_store, template)

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

    def update_content(self, content: List[Dict]) -> None:
        """
        Updates artifact content in storage.

        Args:
            content: New content list to store
        """
        self.content_store.update(self.type, content)

    # get prompt template 
