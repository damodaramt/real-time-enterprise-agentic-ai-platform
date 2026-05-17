from fastapi import FastAPI

app = FastAPI(
    title="Real-Time Enterprise Agentic AI Platform",
    version="0.1.0"
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
