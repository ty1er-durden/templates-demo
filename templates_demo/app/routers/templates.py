from fastapi import APIRouter, Body, HTTPException, Path
from pydantic import BaseModel, constr, Json, Schema
from starlette import status
from typing import Dict, List

FILENAME_REGEX = r"^[\w\-. ]+$"


class Template(BaseModel):
    id: constr(regex=FILENAME_REGEX) = Schema(None, description="Unique Id")
    description: str = Schema(None, description="Brief description of template")
    template: str = Schema(None, description="Body of template")


class Variables(BaseModel):
    variables: Json[Dict]


router = APIRouter()


@router.get("/", response_model=List[Template], summary="Get all templates")
async def read_all():
    return []


@router.get("/{id}", response_model=Template, summary="Get a template")
async def read_one(
    id: str = Path(..., description="Id of the template to retrieve")
):
    result = None
    if isinstance(result, Template):
        return result
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Template,
    summary="Create a template",
    response_description="The new template",
)
async def create_template(template: Template):
    return template


@router.post("/{id}/render", response_model=str, summary="Render a template")
async def render_one(
    *,
    id: str,
    variables: Variables = Body(
        ..., example={"key1": "value1", "key2": "value2"}
    )
):
    """
    Render the template using the Jinja2 engine and the supplied variables
    """
    template = await read_one(id)
    return template
