from contextlib import contextmanager
from typing import Iterator, Any
import mysql.connector
from backend.config import Settings, get_settings


def database_config(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or get_settings()
    return {
        "host": settings.db_host,
        "port": settings.db_port,
        "database": settings.db_name,
        "user": settings.db_user,
        "password": settings.db_password,
    }


@contextmanager
def get_connection(settings: Settings | None = None) -> Iterator[Any]:
    settings = settings or get_settings()
    if not settings.enable_database:
        yield None
        return
    connection = mysql.connector.connect(**database_config(settings))
    try:
        yield connection
    finally:
        connection.close()


def execute_parameterized(query: str, params: tuple[Any, ...], settings: Settings | None = None) -> list[dict[str, Any]]:
    with get_connection(settings) as connection:
        if connection is None:
            return []
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall() if cursor.with_rows else []
        connection.commit()
        cursor.close()
        return rows
