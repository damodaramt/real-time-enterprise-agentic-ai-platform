import psycopg
from psycopg.rows import dict_row

DB_CONFIG = {
    "host": "localhost",
    "port": 5434,
    "dbname": "enterprise_ai",
    "user": "postgres",
    "password": "postgres",
}

CREATE_EXTENSION_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
"""

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(384),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""

CREATE_INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_documents_embedding
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
"""

VERIFY_SQL = """
SELECT
    table_name
FROM information_schema.tables
WHERE table_name = 'documents';
"""


def main() -> None:
    print("Connecting to PostgreSQL...")

    with psycopg.connect(**DB_CONFIG, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            print("Creating vector extension...")
            cur.execute(CREATE_EXTENSION_SQL)

            print("Creating documents table...")
            cur.execute(CREATE_TABLE_SQL)

            print("Creating vector index...")
            cur.execute(CREATE_INDEX_SQL)

            print("Verifying table creation...")
            cur.execute(VERIFY_SQL)
            result = cur.fetchone()

            if not result:
                raise RuntimeError("documents table was not created.")

        conn.commit()

    print("pgvector schema created successfully.")
    print("Table: documents")
    print("Embedding dimension: 384")


if __name__ == "__main__":
    main()
