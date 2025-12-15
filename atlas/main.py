import time
from fastapi import FastAPI

START_TIME = time.time()
VERSION = "0.0.1"

app = FastAPI(title="ATLAS Core", version=VERSION)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": VERSION,
        "uptime_seconds": time.time() - START_TIME,
    }
