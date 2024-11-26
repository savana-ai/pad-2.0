@dataclass
class Prompt:
    template: Dict  # Modified template with context instead of objects
    context: Dict   # Single context item from the referenced artifact