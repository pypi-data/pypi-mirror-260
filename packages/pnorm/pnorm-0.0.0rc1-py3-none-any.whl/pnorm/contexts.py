from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Generator, Optional

if TYPE_CHECKING:
    from pnorm import PostgresClient


@contextmanager
def create_session(
    client: PostgresClient, *, schema: Optional[str] = None
) -> Generator[None, None, None]:
    original_auto_create_connection = client.auto_create_connection
    client.auto_create_connection = False
    close_connection_after_use = False

    if client.connection is None:
        client.create_connection()
        close_connection_after_use = True

    if schema is not None:
        client.set_schema(schema)

    try:
        yield
    except:
        client.rollback()
        raise
    finally:
        if client.connection is not None and close_connection_after_use:
            client.close_connection()

        client.auto_create_connection = original_auto_create_connection


@contextmanager
def create_transaction(client: PostgresClient) -> Generator[None, None, None]:
    client.start_transaction()

    try:
        yield
    except:
        client.rollback()
        raise
    finally:
        client.end_transaction()
