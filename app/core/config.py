import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    # =========================================================
    # Application
    # =========================================================

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "enterprise-ai-platform"
    )

    APP_HOST: str = os.getenv(
        "APP_HOST",
        "0.0.0.0"
    )

    APP_PORT: int = int(
        os.getenv(
            "APP_PORT",
            "8000"
        )
    )

    DEBUG: bool = (
        os.getenv(
            "DEBUG",
            "false"
        ).lower() == "true"
    )

    # =========================================================
    # PostgreSQL
    # =========================================================

    POSTGRES_HOST: str = os.getenv(
        "POSTGRES_HOST",
        "localhost"
    )

    POSTGRES_PORT: int = int(
        os.getenv(
            "POSTGRES_PORT",
            "5432"
        )
    )

    POSTGRES_DB: str = os.getenv(
        "POSTGRES_DB",
        "enterprise_ai"
    )

    POSTGRES_USER: str = os.getenv(
        "POSTGRES_USER",
        "postgres"
    )

    POSTGRES_PASSWORD: str = os.getenv(
        "POSTGRES_PASSWORD",
        "postgres"
    )

    DATABASE_URL: str = (
        f"postgresql://"
        f"{POSTGRES_USER}:"
        f"{POSTGRES_PASSWORD}@"
        f"{POSTGRES_HOST}:"
        f"{POSTGRES_PORT}/"
        f"{POSTGRES_DB}"
    )

    # =========================================================
    # Embeddings
    # =========================================================

    EMBEDDING_MODEL: str = os.getenv(
        "EMBEDDING_MODEL",
        "all-MiniLM-L6-v2"
    )

    EMBEDDING_DIMENSION: int = int(
        os.getenv(
            "EMBEDDING_DIMENSION",
            "384"
        )
    )

    # =========================================================
    # Retrieval
    # =========================================================

    TOP_K_RESULTS: int = int(
        os.getenv(
            "TOP_K_RESULTS",
            "3"
        )
    )

    SIMILARITY_THRESHOLD: float = float(
        os.getenv(
            "SIMILARITY_THRESHOLD",
            "0.90"
        )
    )

    MAX_CONTENT_LENGTH: int = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            "500"
        )
    )

    QUERY_TIMEOUT_SECONDS: int = int(
        os.getenv(
            "QUERY_TIMEOUT_SECONDS",
            "5"
        )
    )

    # =========================================================
    # Langfuse Observability
    # =========================================================

    LANGFUSE_ENABLED: bool = (
        os.getenv(
            "LANGFUSE_ENABLED",
            "false"
        ).lower() == "true"
    )

    LANGFUSE_PUBLIC_KEY: str = os.getenv(
        "LANGFUSE_PUBLIC_KEY",
        ""
    )

    LANGFUSE_SECRET_KEY: str = os.getenv(
        "LANGFUSE_SECRET_KEY",
        ""
    )

    LANGFUSE_HOST: str = os.getenv(
        "LANGFUSE_HOST",
        "https://cloud.langfuse.com"
    )

    # =========================================================
    # MCP
    # =========================================================

    MCP_TIMEOUT_SECONDS: int = int(
        os.getenv(
            "MCP_TIMEOUT_SECONDS",
            "5"
        )
    )


settings = Settings()
