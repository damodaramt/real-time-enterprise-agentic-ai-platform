# Real-Time Enterprise Agentic AI Platform

This enterprise platform demonstrates a production-grade Agentic AI system.

## Architecture Overview

FastAPI receives API requests and user queries.

Apache Kafka is used for real-time event streaming and asynchronous processing.

Kafka consumers process events and invoke AWS Lambda functions.

AWS Lambda performs serverless event processing and business logic.

PostgreSQL with pgvector stores document embeddings and metadata.

Sentence Transformers generate 384-dimensional embeddings using the all-MiniLM-L6-v2 model.

RAG (Retrieval-Augmented Generation) retrieves relevant document chunks.

Model Context Protocol (MCP) connects the AI agent to external tools and services.

Langfuse provides observability for prompts, embeddings, tool calls, and latency.

GitHub Actions automates CI/CD pipelines.

Kubernetes orchestrates all services in production.

Cloudflare Tunnel securely exposes the application to the internet.

## Use Cases

- Enterprise knowledge search
- Telecom network troubleshooting
- API documentation assistant
- Incident response automation
- Intelligent support systems

## Technology Stack

- Python 3.10
- FastAPI
- Apache Kafka
- AWS Lambda
- PostgreSQL
- pgvector
- Sentence Transformers
- MCP
- Langfuse
- GitHub Actions
- Docker
- Kubernetes
- Cloudflare Tunnel
