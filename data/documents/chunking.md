# Document Chunking

## Introduction

Document chunking is the process of splitting large documents into smaller, meaningful sections before generating embeddings. Chunking improves semantic retrieval by allowing the vector database to search relevant portions of a document instead of the entire document.

In this project, chunking is performed before embedding generation and storage in PostgreSQL with the pgvector extension.

---

# Why Chunking?

Large Language Models and embedding models have token limits.

Instead of embedding an entire document, the document is divided into smaller chunks.

Benefits include:

* Better semantic retrieval
* Lower embedding cost
* Improved search accuracy
* Faster indexing
* Reduced token usage

---

# Enterprise RAG Pipeline

Markdown Documents

↓

Document Parser

↓

Text Cleaning

↓

Chunking

↓

Embedding Generation

↓

PostgreSQL + pgvector

↓

Semantic Retrieval

↓

Context Builder

↓

Prompt Builder

↓

OpenAI GPT-4o-mini

↓

Final Response

---

# Chunk Size

Chunk size defines the maximum amount of text stored in one chunk.

Current Project Configuration

Chunk Size

1000 characters

Chunk Overlap

200 characters

These values provide a good balance between retrieval accuracy and context preservation.

---

# Why Overlap?

Without overlap, important information may be split between chunks.

Example

Chunk 1

FastAPI communicates with PostgreSQL using SQL queries.

Chunk 2

SQL queries are optimized using indexes.

Without overlap, the relationship may be lost.

Overlap preserves context across adjacent chunks.

---

# Chunking Workflow

Document

↓

Normalize Text

↓

Remove Extra Spaces

↓

Split into Chunks

↓

Generate Metadata

↓

Generate Embeddings

↓

Store in PostgreSQL

---

# Metadata

Each chunk stores metadata for traceability.

Example

* source
* file_name
* chunk_index
* total_chunks
* embedding_dimension
* model

Metadata helps identify the origin of retrieved information.

---

# Preprocessing

Before chunking:

* Remove unnecessary whitespace
* Normalize line endings
* Remove duplicate spaces
* Preserve headings
* Preserve paragraph structure
* Keep document meaning intact

---

# Chunking Strategies

## Fixed-Length Chunking

Documents are split into equal-sized chunks.

Advantages

* Simple
* Fast
* Easy to implement

Disadvantages

* May split sentences

---

## Recursive Chunking

Splits documents using headings, paragraphs, and sentences before falling back to fixed sizes.

Advantages

* Better semantic boundaries
* Improved retrieval quality

---

## Semantic Chunking

Chunks are created based on meaning rather than size.

Advantages

* Highest retrieval quality

Disadvantages

* Higher computational cost

---

# Best Practices

Use consistent chunk sizes.

Apply chunk overlap.

Keep related information together.

Avoid duplicate chunks.

Store metadata for every chunk.

Use the same chunking strategy during indexing.

Test retrieval quality after ingestion.

---

# Current Project Configuration

Chunk Size

1000 characters

Chunk Overlap

200 characters

Embedding Model

all-MiniLM-L6-v2

Embedding Dimension

384

Database

PostgreSQL + pgvector

---

# Performance Considerations

Monitor:

* Chunk generation time
* Number of chunks created
* Average chunk size
* Embedding generation latency
* Storage usage
* Retrieval latency

---

# Common Problems

Chunks too large

* Higher token usage
* Poor retrieval precision

Chunks too small

* Loss of context
* Lower answer quality

No overlap

* Missing relationships between adjacent chunks

Duplicate chunks

* Repeated retrieval results

---

# Enterprise Use Cases

Technical documentation

API documentation

Internal knowledge bases

Policy documents

Healthcare records

Financial reports

Legal documents

Product manuals

---

# Future Improvements

Recursive document chunking

Semantic chunking

Language-aware chunking

Table-aware chunking

PDF structure preservation

Automatic heading detection

Incremental document updates

Hybrid retrieval optimization

---

# Current Project Flow

Markdown Documents

↓

Chunking Service

↓

Embedding Service

↓

PostgreSQL + pgvector

↓

Retrieval Service

↓

Context Builder

↓

Prompt Builder

↓

OpenAI GPT-4o-mini

↓

Response

---

# Summary

Document chunking is one of the most important stages in a Retrieval-Augmented Generation system. Proper chunk sizes, overlap, metadata, and preprocessing significantly improve retrieval accuracy and overall answer quality in enterprise AI platforms.

