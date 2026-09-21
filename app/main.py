from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.products import router as products_router

app = FastAPI(
    title="Backend Platform API",
    version="0.3.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(auth_router)
app.include_router(products_router)
