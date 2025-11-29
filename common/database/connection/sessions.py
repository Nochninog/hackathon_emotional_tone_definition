from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionMaker:
    __session_maker: ClassVar[async_sessionmaker[AsyncSession]]

    @classmethod
    def get_session_maker(cls) -> async_sessionmaker[AsyncSession]:
        return cls.__session_maker

    @classmethod
    def set_session_maker(cls, session_maker: async_sessionmaker[AsyncSession]) -> None:
        cls.__session_maker = session_maker
