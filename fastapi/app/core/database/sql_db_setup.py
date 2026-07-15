from contextlib import asynccontextmanager, contextmanager

from sqlalchemy import create_engine
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.exceptions import AppException
from config import settings

ssl_mode = "require" if settings.db_ssl else "prefer"

engine_kwargs = (
    dict(pool_size=15, max_overflow=5, pool_pre_ping=True)
    if settings.db_connection_pool
    else dict(poolclass=NullPool)
)


class Base(DeclarativeBase):
    pass


def make_engine(uri: str, *, async_: bool):
    if settings.db_type == "sqlite":
        # SQLite-specific connect args
        connect_args = settings.SQLITE_CONNECT_ARGS
    else:
        # PostgreSQL connect args with SSL
        connect_args = {"sslmode": ssl_mode} if not async_ else {"ssl": ssl_mode}

    if async_:
        engine = create_async_engine(uri, **engine_kwargs, connect_args=connect_args)
        session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    else:
        engine = create_engine(uri, **engine_kwargs, connect_args=connect_args)
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, session


db_engine, SessionLocal = make_engine(
    uri=settings.SQLALCHEMY_DATABASE_URI, async_=settings.db_async_connection
)


@contextmanager
def db_sync_session():
    db = SessionLocal()
    try:
        yield db
    except (DBAPIError, IntegrityError) as exc:
        db.rollback()
        raise AppException.BadRequestException(
            error_message=f"DatabaseError({exc.orig.args[0]})"
        )
    finally:
        db.close()


@asynccontextmanager
async def db_async_session():
    async with SessionLocal() as async_session:
        try:
            yield async_session
        except (DBAPIError, IntegrityError) as exc:
            await async_session.rollback()
            raise AppException.BadRequestException(
                error_message=f"DatabaseError({exc.orig.args[0]})",
                context=f"DatabaseError({exc})",
            )