# remove_bg_route.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/remove_bg", tags=["Remove Background"])

class RemoveBGRequest(BaseModel):
    image: str
    preserve_alpha: bool | None = False
    sync: bool | None = True
    visual_input_content_moderation: bool | None = False
    visual_output_content_moderation: bool | None = False

@router.post("/")
def remove_bg_route(payload: RemoveBGRequest):
    try:
        result = bria_edit("remove_bg", payload.dict(exclude_none=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
