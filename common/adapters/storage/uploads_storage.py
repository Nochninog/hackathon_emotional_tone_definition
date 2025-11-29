from abc import ABC, abstractmethod
from collections.abc import Sequence

from ...domain.models import Upload, UploadStatus


class IUploadStorage(ABC):
    @abstractmethod
    async def create_upload(
        self,
        status: UploadStatus,
        filename: str,
        has_validation: bool = False,
    ) -> Upload:
        raise NotImplementedError

    @abstractmethod
    async def get_all_uploads(
        self,
    ) -> Sequence[Upload]:
        raise NotImplementedError

    @abstractmethod
    async def get_upload_by_id(
        self,
        upload_id: int,
    ) -> Upload:
        raise NotImplementedError

    @abstractmethod
    async def update_upload_status(
        self,
        upload_id: int,
        status: UploadStatus,
    ) -> None:
        raise NotImplementedError
