from pydantic import BaseModel
from typing import Optional, Union, List
from fastapi import APIRouter, HTTPException
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/expand", tags=["Expand Image"])

class ExpandRequest(BaseModel):
    image: str
    aspect_ratio: Optional[Union[str, float]] = None  # "1:1", "2:3", etc. or custom float
    prompt: Optional[str] = None
    seed: Optional[int] = None
    negative_prompt: Optional[str] = None
    preserve_alpha: Optional[bool] = False
    sync: Optional[bool] = True
    visual_input_content_moderation: Optional[bool] = False
    visual_output_content_moderation: Optional[bool] = False

@router.post("/")
def expand_route(payload: ExpandRequest):
    try:
        result = bria_edit("expand", payload.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))