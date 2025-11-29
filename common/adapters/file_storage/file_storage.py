from abc import ABC, abstractmethod


class IFileStorage(ABC):
    @abstractmethod
    async def save_upload_file(self, content: bytes, upload_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_upload_file(self, upload_id: int) -> bytes:
        raise NotImplementedError

    @abstractmethod
    async def save_validation_file(self, content: bytes, upload_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def read_validation_file(self, upload_id: int) -> bytes:
        raise NotImplementedError
