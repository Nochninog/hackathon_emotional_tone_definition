from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(
    db_url: str,
) -> AsyncEngine:
    return create_async_engine(
        url=db_url,
        echo=False,
        pool_pre_ping=True,
    )


def create_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )



async def dispose_engine(engine: AsyncEngine) -> None:
    await engine.dispose()
