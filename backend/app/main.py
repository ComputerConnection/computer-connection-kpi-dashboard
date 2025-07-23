from fastapi import FastAPI

from .auth import router as auth_router
from .auth.middleware import auth_middleware

app = FastAPI()

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.middleware("http")(auth_middleware)
