import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    APP_NAME = os.getenv(
        "APP_NAME",
        "enterprise-ai-platform"
    )

    APP_HOST = os.getenv(
        "APP_HOST",
        "0.0.0.0"
    )

    APP_PORT = int(
        os.getenv(
            "APP_PORT",
            "8000"
        )
    )

    DEBUG = (
        os.getenv(
            "DEBUG",
            "false"
        ).lower() == "true"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    POSTGRES_HOST = os.getenv(
        "POSTGRES_HOST",
        "localhost"
    )

    POSTGRES_PORT = int(
        os.getenv(
            "POSTGRES_PORT",
            "5432"
        )
    )

    POSTGRES_DB = os.getenv(
        "POSTGRES_DB",
        "enterprise_ai"
    )

    POSTGRES_USER = os.getenv(
        "POSTGRES_USER",
        "postgres"
    )

    POSTGRES_PASSWORD = os.getenv(
        "POSTGRES_PASSWORD",
        "postgres"
    )

    DATABASE_URL = (
        f"postgresql://"
        f"{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/"
        f"{POSTGRES_DB}"
    )

    EMBEDDING_MODEL = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2"
    )

    EMBEDDING_DIMENSION = int(
        os.getenv(
            "EMBEDDING_DIMENSION",
            "384"
        )
    )

    TOP_K_RESULTS = int(
        os.getenv(
            "TOP_K_RESULTS",
            "5"
        )
    )

    SIMILARITY_THRESHOLD = float(
        os.getenv(
            "SIMILARITY_THRESHOLD",
            "0.90"
        )
    )

    MAX_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            "1000"
        )
    )

    QUERY_TIMEOUT_SECONDS = int(
        os.getenv(
            "QUERY_TIMEOUT_SECONDS",
            "10"
        )
    )

    OPENAI_API_KEY = os.getenv(
        "OPENAI_API_KEY",
        ""
    )

    OPENAI_MODEL = os.getenv(
        "OPENAI_MODEL",
        "gpt-4o-mini"
    )

    OPENAI_TEMPERATURE = float(
        os.getenv(
            "OPENAI_TEMPERATURE",
            "0.0"
        )
    )

    OPENAI_MAX_TOKENS = int(
        os.getenv(
            "OPENAI_MAX_TOKENS",
            "1500"
        )
    )

    ENABLE_STREAMING = (
        os.getenv(
            "ENABLE_STREAMING",
            "true"
        ).lower() == "true"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        ""
    )

    JWT_ALGORITHM = os.getenv(
        "JWT_ALGORITHM",
        "HS256"
    )

    JWT_EXPIRE_MINUTES = int(
        os.getenv(
            "JWT_EXPIRE_MINUTES",
            "60"
        )
    )

    LANGFUSE_ENABLED = (
        os.getenv(
            "LANGFUSE_ENABLED",
            "false"
        ).lower() == "true"
    )

    LANGFUSE_PUBLIC_KEY = os.getenv(
        "LANGFUSE_PUBLIC_KEY",
        ""
    )

    LANGFUSE_SECRET_KEY = os.getenv(
        "LANGFUSE_SECRET_KEY",
        ""
    )

    LANGFUSE_HOST = os.getenv(
        "LANGFUSE_HOST",
        "https://cloud.langfuse.com"
    )

    MCP_TIMEOUT_SECONDS = int(
        os.getenv(
            "MCP_TIMEOUT_SECONDS",
            "10"
        )
    )


settings = Settings()
