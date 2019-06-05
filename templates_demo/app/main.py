from fastapi import FastAPI
from pydantic import BaseModel
from routers import templates, version


class Message(BaseModel):
    detail: str


app = FastAPI()

app.include_router(version.router, prefix="/version")
app.include_router(
    templates.router,
    prefix="/templates",
    responses={404: {"description": "Not found", "model": Message}},
)
