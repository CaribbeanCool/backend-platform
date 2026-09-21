from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.middleware.request_id import RequestIDMiddleware
from app.routes.auth import router as auth_router
from app.routes.products import router as products_router

app = FastAPI(
    title="Backend Platform API",
    version="0.3.0",
)

app.add_middleware(RequestIDMiddleware)

Instrumentator().instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=False,
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(products_router)
