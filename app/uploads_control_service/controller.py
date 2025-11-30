from __future__ import annotations

from dataclasses import asdict
from typing import TYPE_CHECKING, Annotated

from fastapi import Body, File, HTTPException, Path, Query, UploadFile, status

from common.api.controller import BaseController
from common.api.schemas import SToneDistribution, SUpload, SUploadProcessingProgress
from common.usecases import (
    create_upload_usecase,
    get_tone_distribution_usecase,
    get_upload_processing_progress_usecase,
    get_upload_sources_usecase,
    list_uploads_usecase,
    retrieve_upload_usecase,
)

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
            *,
            has_validation: Annotated[bool, Body()] = False,
        ) -> SUpload:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                upload_file_bytes = await upload_file.read()
                upload = await create_upload_usecase(
                    uow=uow,
                    file_storage=self.__file_storage,
                    event_publisher=self.__event_publisher,
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

        @self._router.get(
            path="/uploads/{upload_id}/",
            response_model=SUpload,
        )
        async def get_upload(
            upload_id: Annotated[int, Path()],
        ) -> SUpload:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                try:
                    upload = await retrieve_upload_usecase(
                        uow=uow,
                        upload_id=upload_id,
                    )
                except ValueError as e:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                    ) from e

                return SUpload.model_validate(asdict(upload))

        @self._router.get(
            path="/uploads/{upload_id}/progress/",
            response_model=SUploadProcessingProgress,
        )
        async def get_upload_processing_progress(
            upload_id: Annotated[int, Path()],
        ) -> SUploadProcessingProgress:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                model = await get_upload_processing_progress_usecase(
                    uow=uow,
                    upload_id=upload_id,
                )
                return SUploadProcessingProgress.model_validate(asdict(model))

        @self._router.get(
            path="/uploads/{upload_id}/tones/",
            response_model=SToneDistribution,
        )
        async def get_tone_distribution(
            upload_id: Annotated[int, Path()],
        ) -> SToneDistribution:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                model = await get_tone_distribution_usecase(
                    uow=uow,
                    upload_id=upload_id,
                )
                return SToneDistribution.model_validate(asdict(model))

        @self._router.get(
            path="/uploads/{upload_id}/sources/",
            response_model=list[str],
        )
        async def get_upload_sources(
            upload_id: Annotated[int, Path()],
        ) -> list[str]:
            async with self.__unit_of_work_factory.with_unit_of_work() as uow:
                sources = await get_upload_sources_usecase(
                    uow=uow,
                    upload_id=upload_id,
                )
                return list(sources)
