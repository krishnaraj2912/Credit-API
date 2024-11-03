from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from application.core.setting import settings
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(settings.DB_URL, echo=False)

async def get_db():
    asyncSessionLocal = async_sessionmaker(bind=engine, autocommit=False, expire_on_commit=False)
    async with asyncSessionLocal() as asyncSession:
        try:
            yield asyncSession
        finally:
            await asyncSession.close()

Base = declarative_base()
db_dependency = Annotated[AsyncSession, Depends(get_db)]