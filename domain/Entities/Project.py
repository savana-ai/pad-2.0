# project store 

# domain/project.py
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
        self.content_store.update(
            ArtifactType.QUESTIONNAIRE, 
            [questionnaire_content]
        )

    # get context 

    