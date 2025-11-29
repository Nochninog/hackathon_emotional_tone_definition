from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Annotated

from fastapi import Body, File, Query, UploadFile

from common.api.controller import BaseController
from common.api.schemas import SUpload
from common.usecases import create_upload_usecase, list_uploads_usecase

if TYPE_CHECKING:
    from common.adapters.events import IEventPublisher
    from common.adapters.file_storage import IFileStorage
    from common.adapters.parser import IUploadParser
    from common.adapters.storage import IUnitOfWork, IUnitOfWorkFactory


class UploadsController(BaseController):

    __file_storage: IFileStorage
    __event_publisher: IEventPublisher
    __unit_of_work_factory: IUnitOfWorkFactory[IUnitOfWork]
    __upload_parser: IUploadParser

    def __init__(
        self,
        file_storage: IFileStorage,
        event_publisher: IEventPublisher,
        unit_of_work_factory: IUnitOfWorkFactory[IUnitOfWork],
        upload_parser: IUploadParser,
    ) -> None:
        super().__init__()

        self.__upload_parser = upload_parser
        self.__file_storage = file_storage
        self.__event_publisher = event_publisher
        self.__unit_of_work_factory = unit_of_work_factory

        @self._router.post(
            path="/uploads/",
            response_model=SUpload,
        )
        async def create_upload(
            upload_file: Annotated[UploadFile, File()],
            *,
            has_validation: Annotated[bool, Body()] = False,
        ) -> SUpload:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                upload_file_bytes = await upload_file.read()
                upload = await create_upload_usecase(
                    uow=uow,
                    file_storage=self.__file_storage,
                    event_publisher=self.__event_publisher,
                    upload_parser=self.__upload_parser,
                    upload_file_bytes=upload_file_bytes,
                    upload_filename=str(upload_file.filename),
                    has_validation=has_validation,
                )

                return SUpload.model_validate(asdict(upload))

        @self._router.get(
            path="/uploads/",
            response_model=list[SUpload],
        )
        async def get_all_uploads(
            search: Annotated[str, Query()] = "",
        ) -> list[SUpload]:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                uploads = await list_uploads_usecase(
                    uow=uow,
                    search=search,
                )

                return [
                    SUpload.model_validate(asdict(upload))
                    for upload in uploads
                ]
