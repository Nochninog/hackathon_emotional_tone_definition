from pathlib import Path

from aiopath import AsyncPath

from ...adapters.file_storage import IFileStorage


class LocalFileStorage(IFileStorage):
    __async_path: AsyncPath

    def __init__(self, path_to_uploads: str) -> None:
        self.__async_path = AsyncPath(path_to_uploads)
        sync_path = Path(path_to_uploads)

        if not sync_path.exists():
            raise FileNotFoundError

    async def read_upload_file(self, upload_id: int) -> bytes:
        path_to_file = self.__make_upload_filepath(upload_id=upload_id)
        if not await path_to_file.exists():
            raise FileNotFoundError

        return await path_to_file.read_bytes()  # type: ignore[no-any-return]

    async def save_upload_file(self, content: bytes, upload_id: int) -> None:
        path_to_file = self.__make_upload_filepath(upload_id=upload_id)
        if await path_to_file.exists():
            raise FileExistsError

        path_to_file.write_bytes(content)

    async def read_validation_file(self, upload_id: int) -> bytes:
        path_to_file = self.__make_validation_filepath(upload_id=upload_id)
        if not await path_to_file.exists():
            raise FileNotFoundError

        return await path_to_file.read_bytes()  # type: ignore[no-any-return]

    async def save_validation_file(self, content: bytes, upload_id: int) -> None:
        path_to_file = self.__make_validation_filepath(upload_id=upload_id)
        if await path_to_file.exists():
            raise FileExistsError

        path_to_file.write_bytes(content)

    def __make_upload_filepath(self, upload_id: int) -> AsyncPath:
        return self.__async_path / "uploads" / f"upload_{upload_id}.csv"

    def __make_validation_filepath(self, upload_id: int) -> AsyncPath:
        return self.__async_path / "validations" / f"validation_{upload_id}.csv"