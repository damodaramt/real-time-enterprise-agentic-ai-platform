import logging

import psycopg
from psycopg import Connection

from app.core.config import settings


logger = logging.getLogger(__name__)


def get_db_connection() -> Connection:
    """
    Create PostgreSQL connection.
    """

    try:

        connection = psycopg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            autocommit=False
        )

        logger.info(
            "PostgreSQL connection established."
        )

        return connection

    except Exception as error:

        logger.exception(
            "Database connection failed: %s",
            str(error)
        )

        raise
