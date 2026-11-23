from fastapi import FastAPI

app = FastAPI(title="Schedule App API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}