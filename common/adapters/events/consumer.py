from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable


class IEventConsumer(ABC):
    @abstractmethod
    def register_event(
        self,
        event_name: str,
        handler: Callable[[Any], Any],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_consuming(
        self,
    ) -> None:
        raise NotImplementedError
