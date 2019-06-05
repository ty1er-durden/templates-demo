from fastapi import APIRouter
from pydantic import BaseModel, constr

SIMPLE_SEMVER_REGEX = r"^[0-9]+\.[0-9]+\.[0-9]+$"
VERSION = "0.1.0"


class Version(BaseModel):
    name: str
    version: constr(regex=SIMPLE_SEMVER_REGEX)


router = APIRouter()


@router.get("/", summary="Get API version", response_model=Version)
async def read_version():
    return {"name": "Templates Demo", "version": VERSION}
