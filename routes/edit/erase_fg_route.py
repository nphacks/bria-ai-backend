from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, HTTPException
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/erase_fg", tags=["Erase Foreground"])

class EraseFGRequest(BaseModel):
    image: str
    preserve_alpha: Optional[bool] = False
    sync: Optional[bool] = True
    visual_input_content_moderation: Optional[bool] = False
    visual_output_content_moderation: Optional[bool] = False


@router.post("/")
def erase_fg_route(payload: EraseFGRequest):
    try:
        result = bria_edit("erase_fg", payload.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))