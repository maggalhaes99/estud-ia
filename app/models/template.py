import uuid
from typing import List, Optional

class TemplateAnnotation:
    def __init__(
        self,
        nome: str,
        perguntas: Optional[List[str]] = None,
        id: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.perguntas = perguntas or []