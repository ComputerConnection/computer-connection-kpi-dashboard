from fastapi import FastAPI

from .auth import router as auth_router
from .auth.middleware import auth_middleware
from .audit import router as audit_router
from .api.graphql.router import router as graphql_router
from .actions.router import router as actions_router

app = FastAPI()


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(audit_router)
app.include_router(graphql_router)
app.include_router(actions_router)
app.middleware("http")(auth_middleware)
