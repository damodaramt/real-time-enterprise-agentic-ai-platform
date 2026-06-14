# Redis

## Introduction

Redis (Remote Dictionary Server) is an open-source, in-memory data store used as a cache, message broker, and lightweight database. It stores data in memory, making read and write operations extremely fast.

In enterprise AI platforms, Redis is commonly used to cache frequently accessed data, reduce database load, improve API response times, and support background processing.

---

# Why Redis?

Without Redis, every request may query PostgreSQL or call the LLM.

Example

User

↓

FastAPI

↓

PostgreSQL

↓

OpenAI

↓

Response

When the same question is asked repeatedly, Redis can return the cached response immediately.

Benefits include:

* Faster response times
* Reduced database load
* Lower API costs
* Better scalability
* Improved user experience

---

# Redis Architecture

Client

↓

FastAPI

↓

Redis Cache

↓

PostgreSQL

↓

OpenAI

↓

Response

---

# Key-Value Storage

Redis stores information as key-value pairs.

Example

Key

question:what_is_docker

Value

Docker is a containerization platform...

This allows very fast retrieval.

---

# In-Memory Storage

Redis stores data in RAM instead of disk.

Advantages

* Extremely low latency
* High throughput
* Millions of operations per second

Because memory is limited, Redis is usually used as a cache rather than permanent storage.

---

# Time To Live (TTL)

TTL defines how long a cached item remains available.

Example

Question Cache

10 minutes

Embedding Cache

30 minutes

Session Cache

1 hour

After the TTL expires, Redis automatically removes the entry.

---

# Cache Invalidation

Sometimes cached data becomes outdated.

Common invalidation strategies:

* Time-based expiration
* Manual deletion
* Update on write
* Refresh after document ingestion

Correct cache invalidation ensures users receive current information.

---

# Pub/Sub

Redis supports Publish/Subscribe messaging.

Components

Publisher

↓

Redis Channel

↓

Subscribers

Enterprise use cases:

* Notifications
* Real-time updates
* Chat systems
* Event processing

---

# Session Management

Redis can store user sessions.

Example

Session ID

↓

User Information

↓

Expiration Time

Benefits

* Fast authentication
* Shared sessions across servers
* Scalable web applications

---

# Rate Limiting

Redis is commonly used to implement API rate limiting.

Example

Maximum

100 requests per minute

If exceeded

Return HTTP 429

This protects APIs from abuse.

---

# Redis in Enterprise RAG

Redis can cache:

* User questions
* LLM responses
* Query embeddings
* Retrieved document IDs
* Prompt templates
* Authentication sessions

This reduces repeated computation.

---

# Current Project Architecture

User

↓

FastAPI

↓

Redis Cache

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

Streaming Response

---

# Enterprise Use Cases

* API caching
* Session storage
* Background job queues
* Real-time notifications
* Rate limiting
* Leaderboards
* Chat applications
* AI response caching

---

# Best Practices

Use Redis only for temporary data.

Set TTL for cached entries.

Monitor memory usage.

Avoid storing sensitive data without protection.

Use descriptive cache keys.

Invalidate cache after document updates.

Monitor cache hit ratio.

---

# Monitoring

Monitor

* Memory usage
* Cache hit ratio
* Cache miss ratio
* Expired keys
* Connected clients
* Request latency
* Evicted keys

---

# Advantages

Very fast

Low latency

Easy integration

Scalable

Open source

Supports multiple data structures

Production ready

---

# Current Project Usage

Planned Redis usage:

* Cache semantic search results
* Cache OpenAI responses
* Store user sessions
* Cache prompt templates
* Reduce PostgreSQL queries
* Improve API performance

---

# Future Improvements

Distributed Redis Cluster

High Availability

Redis Sentinel

Background task queues

Streaming event processing

Shared cache across Kubernetes pods

---

# Summary

Redis is a high-performance in-memory data store that improves enterprise AI systems by caching frequently accessed data, reducing latency, lowering database load, and minimizing repeated LLM requests. It is a key component in scalable Retrieval-Augmented Generation platforms.

