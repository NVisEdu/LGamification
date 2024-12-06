from Controllers.api_models import journal_dto
from Models.ActionLog import ActionLogRepository
from abstractions import FacadeAbstract


class JournalFacade(FacadeAbstract):
    Repo = ActionLogRepository()
    model = Repo.model
    entry: model
    dto = journal_dto

    def __init__(self, obj: model):
        self.entry = obj

    @staticmethod
    def get(ID: int) -> "JournalFacade":
        return JournalFacade(ActionLogRepository().get(ID))

    def delete(self):
        self.Repo.delete(self.entry)
        del self

    @staticmethod
    def get_by_user(userID: int, limit: int = 100):
        return JournalFacade.Repo.get_all_by_user(userID, limit)
