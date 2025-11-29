from collections.abc import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ...adapters.storage import IUploadStorage
from ...domain.models import Upload, UploadStatus

from ..models import UploadORM
from ..mappers import upload_orm_to_model, upload_orms_to_models


class SqlAlchemyUploadStorage(IUploadStorage):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_upload(
        self,
        status: UploadStatus,
        filename: str,
        has_validation: bool = False,
    ) -> Upload:
        upload = UploadORM(
            status=status,
            filename=filename,
            has_validation=has_validation,
        )

        self._session.add(upload)
        await self._session.flush()

        return upload_orm_to_model(upload)

    async def get_all_uploads(
        self,
    ) -> Sequence[Upload]:
        query = select(UploadORM)
        uploads = await self._session.scalars(query)
        return upload_orms_to_models(uploads)

    async def get_upload_by_id(
        self,
        upload_id: int,
    ) -> Upload:
        query = select(UploadORM).where(UploadORM.upload_id == upload_id)
        upload = await self._session.scalar(query)

        if upload is None:
            raise ValueError(f"Upload with id={upload_id} not found")

        return upload_orm_to_model(upload)

    async def update_upload_status(
        self,
        upload_id: int,
        status: UploadStatus,
    ) -> None:
        query = (
            update(UploadORM)
            .where(UploadORM.upload_id == upload_id)
            .values(status=status)
        )

        await self._session.execute(query)
