from domain.Entities.Project import Project
from typing import Dict

class ProjectInitializationService:
    def __init__(self, user_response: Dict):
        """
        Initialize Project Initialization Service
        
        Args:
            user_response (Dict): User's response containing project details
        """
        self.user_response = user_response

    def initialize_project(self) -> Project:
        """
        Initialize a project based on user response
        
        Returns:
            Project: Initialized project instance
        """
        # Extract project name and questionnaire from user_response
        project_name = self.user_response.get('project_name')
        questionnaire_content = self.user_response.get('questionnaire')
        
        if not project_name:
            raise ValueError("Project name is required")
        
        # Create Project instance
        project = Project(name=project_name)
        
        # Initialize with questionnaire if available
        if questionnaire_content:
            project.initialize_with_questionnaire(questionnaire_content)
        
        return project


if __name__ == "__main__":
    # Sample user response for initializing the project
    user_response = {
        "project_name": "New AI Project",
        "questionnaire": {
            "purpose": "Build an AI-powered chatbot",
            "features": ["Natural Language Processing", "Integration with CRM"],
            "deadline": "2024-12-31"
        }
    }

    # Initialize the service with the user response
    service = ProjectInitializationService(user_response=user_response)

    # Call the initialize_project method and print the result
    try:
        project = service.initialize_project()
        print(f"Project initialized successfully:\nName: {project.name}")
        if hasattr(project, 'get_questionnaire_content'):
            print(f"Questionnaire: {project.get_questionnaire_content()}")
    except Exception as e:
        print(f"Project initialization failed: {e}")
