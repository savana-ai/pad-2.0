from typing import Dict, Any, List
from domain.Entities.Artifact import Artifact
from domain.Entities.Project import Project
from infrastructure.http.request import ExternalServiceClient
from domain.value_objects.artifact_type import ArtifactType

class ArtifactGenerationService:
    def __init__(self,
                 project_name: str,
                 artifact_type: ArtifactType,
                 llm_service: str,
                 additional_context: Dict[str, Any] = None):
        """
        Initialize the Artifact Generation Service
        
        Args:
            project_name (str): Name of the project
            artifact_type (ArtifactType): Type of artifact to generate
            llm_service (str): The LLM service to use for generation
            additional_context (Dict[str, Any], optional): Additional context for artifact generation
        """
        self.project_name = project_name
        self.artifact_type = artifact_type
        self.llm_service = llm_service
        self.additional_context = additional_context or {}

    def generate_artifact(self) -> bool:
        """
        Generate an artifact for the project
        
        Returns:
            bool: Whether artifact generation was successful
        """
        # Create an Artifact instance (without project_id)
        artifact = Artifact(type=self.artifact_type)
        
        # Get prompt templates
        templates = artifact.get_prompts()
        
        # Create a Project instance
        project = Project(name=self.project_name, description="")
        
        # Get project context
        context = project.get_content(self.artifact_type)
        
        # If no context is found, use additional context if available
        if not context and self.additional_context:
            context = [self.additional_context]
        
        # Ensure context exists
        if not context:
            raise ValueError(f"No context found for artifact type {self.artifact_type}")
        
        # Create prompts
        prompts = artifact.create_prompt(templates[0], context)
        
        # Send to LLM service
        request_handler = ExternalServiceClient(llm_service)
        content = request_handler.request(prompts)
        
        # Update project content
        project.update_content(content, self.artifact_type)
        
        return True



if __name__ == "__main__":
    # Input parameters for the service
    project_name = "Test Project"
    artifact_type = ArtifactType("Documentation")  # Replace with a valid artifact type if needed
    llm_service = "https://example-llm-service.com/api"
    additional_context = {
        "key1": "value1",
        "key2": "value2",
    }

    # Instantiate the ArtifactGenerationService
    service = ArtifactGenerationService(
        project_name=project_name,
        artifact_type=artifact_type,
        llm_service=llm_service,
        additional_context=additional_context
    )

    # Call the generate_artifact method and print the result
    try:
        result = service.generate_artifact()
        print(f"Artifact generation success: {result}")
    except Exception as e:
        print(f"Artifact generation failed: {e}")
