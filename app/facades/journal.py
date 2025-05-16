from app.schemas.api_models import journal_dto
from app.models import ActionLogRepository
from app.core.abstractions import FacadeAbstract


class JournalFacade(FacadeAbstract):
    repo = ActionLogRepository()
    entry: repo.model
    dto = journal_dto

    def __init__(self, obj: repo.model):
        super().__init__(obj)

    @classmethod
    def get(cls, ID: int) -> "JournalFacade":
        return cls(ActionLogRepository().get(ID))

    def delete(self):
        self.repo.delete(self.entry)
        del self

    @classmethod
    def get_by_user(cls, userID: int, limit: int = 100):
        return cls.repo.get_all_by_user(userID, limit)
