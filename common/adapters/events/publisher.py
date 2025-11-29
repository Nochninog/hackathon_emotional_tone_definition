from abc import ABC, abstractmethod
from typing import Any


class IEventPublisher(ABC):
    @abstractmethod
    async def publish_event(
        self,
        event_name: str,
        data: Any,
    ) -> None:
        raise NotImplementedError
