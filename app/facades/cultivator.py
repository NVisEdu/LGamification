
from app.core.abstractions import FacadeAbstract
from app.models.unused.cultivator import CultivatorRepository
from app.schemas.api_models import cultivator_dto


class CultivatorFacade(FacadeAbstract):
    repo = CultivatorRepository
    dto = cultivator_dto

    entry: CultivatorRepository.model

    def __init__(self, obj: repo.model):
        super().__init__(obj)

    @classmethod
    def get(cls, ID: int) -> "CultivatorFacade":
        return cls(cls.repo.get(ID))

    @classmethod
    def create(cls, userID: int, title: str,
               xp_reward: int,
               hp_penalty: int) -> "CultivatorFacade":
        return cls(
            cls.repo.create(userID, title, xp_reward, hp_penalty)
        )

    @classmethod
    def get_all_by_user(cls, user_ID) -> tuple["CultivatorFacade", ...]:
        return tuple(
            cls(i) for i in cls.repo.get_all_by_user(user_ID)
        )

    def complete(self):
        self.repo.edit(self.entry, status="Done")

    def to_dict(self):
        res = self.entry.__dict__
        return res
