from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Annotated

from fastapi import Body, File, UploadFile, Query

from common.api.controller import BaseController
from common.api.schemas import SUpload, SUploadCreate
from common.usecases import create_upload_usecase

if TYPE_CHECKING:
    from common.adapters.events import IEventPublisher
    from common.adapters.file_storage import IFileStorage
    from common.adapters.storage import IUnitOfWork, IUnitOfWorkFactory


class UploadsController(BaseController):

    __file_storage: IFileStorage
    __event_publisher: IEventPublisher
    __unit_of_work_factory: IUnitOfWorkFactory[IUnitOfWork]

    def __init__(
        self,
        file_storage: IFileStorage,
        event_publisher: IEventPublisher,
        unit_of_work_factory: IUnitOfWorkFactory[IUnitOfWork],
    ) -> None:
        super().__init__()

        self.__file_storage = file_storage
        self.__event_publisher = event_publisher
        self.__unit_of_work_factory = unit_of_work_factory

        @self._router.post(
            path="/uploads/",
            response_model=SUpload,
        )
        async def create_upload(
            upload_file: Annotated[UploadFile, File()],
            validation_file: Annotated[UploadFile | None, File()] = None,
        ) -> SUpload:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                upload_file_bytes = await upload_file.read()
                validation_file_bytes = (
                    await validation_file.read()
                    if validation_file is not None else None
                )
                upload = await create_upload_usecase(
                    uow=uow,
                    file_storage=self.__file_storage,
                    event_publisher=self.__event_publisher,
                    upload_file_bytes=upload_file_bytes,
                    upload_filename=str(upload_file.filename),
                    validation_file_bytes=validation_file_bytes,
                    has_validation=validation_file is not None,
                )

                return SUpload.model_validate(asdict(upload))

        @self._router.get(
            path="/uploads/",
            response_model=list[SUpload],
        )
        async def get_all_uploads(
            search: Annotated[str, Query()] = "",
        ) -> list[SUpload]:
            pass