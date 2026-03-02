from app.repositories.template_annotation_repository import TemplateAnnotationRepository
from app.models.template import TemplateAnnotation

class TemplateAnnotationService:

    def __init__(self):
        self.repo = TemplateAnnotationRepository()

    def list_all(self) -> list[TemplateAnnotation]:
        return self.repo.get_all()

    def create(self, template: TemplateAnnotation) -> None:
        self._validate(template)
        self.repo.insert(template)

    def _validate(self, template: TemplateAnnotation) -> None:
        if not template.nome or not template.nome.strip():
            raise ValueError("O nome do template é obrigatório.")

        perguntas_validas = [
            p.strip()
            for p in template.perguntas
            if p and p.strip()
        ]

        if not perguntas_validas:
            raise ValueError("O template deve ter ao menos uma pergunta.")

        template.perguntas = perguntas_validas