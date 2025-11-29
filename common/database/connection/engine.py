from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .sessions import SessionMaker


def create_engine(
    db_name: str,
    db_user: str,
    db_password: str,
    db_host: str,
    db_port: int,
    db_engine: str,
) -> AsyncEngine:
    db_url = f"{db_engine}://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_async_engine(
        url=db_url,
        echo=False,
        pool_pre_ping=True,
    )

    SessionMaker.set_session_maker(
        async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        ),
    )

    return engine


async def dispose_engine(engine: AsyncEngine) -> None:
    await engine.dispose()
