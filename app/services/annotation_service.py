from app.repositories.annotation_repository import AnnotationRepository
from app.models.annotation import Annotation

class AnnotationService:

    def __init__(self):
        self.repo = AnnotationRepository()

    def create(self, annotation: Annotation):
        self.repo.insert(annotation)

    def update(self, annotation: Annotation):
        self.repo.update_secoes(annotation)

    def delete(self, annotation_id: str):
        self.repo.delete(annotation_id)

    def list_all(self):
        return self.repo.get_all()

    def search(self, text: str):
        return self.repo.search(text)