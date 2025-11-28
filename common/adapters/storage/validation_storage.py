from abc import ABC, abstractmethod
from collections.abc import Iterable, Sequence

from ....domain.models import Validation


class IValidationStorage(ABC):
    @abstractmethod
    async def create_validations(
        self,
        text_ids: Iterable[int],
        labels: Iterable[int],
    ) -> Sequence[Validation]:
        raise NotImplementedError

    @abstractmethod
    async def get_validation_for_text(
        self,
        text_id: int,
    ) -> Validation:
        raise NotImplementedError
    
    @abstractmethod
    async def get_validations_for_texts(
        self,
        text_ids: int,
    ) -> Validation:
        raise NotImplementedError
