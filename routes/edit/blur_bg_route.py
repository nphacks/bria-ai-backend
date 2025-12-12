from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, HTTPException
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/blur_bg", tags=["Blur Background"])

class BlurBGRequest(BaseModel):
    image: str
    scale: Optional[int] = None  # 1-5
    preserve_alpha: Optional[bool] = False
    sync: Optional[bool] = True
    visual_input_content_moderation: Optional[bool] = False
    visual_output_content_moderation: Optional[bool] = False

@router.post("/")
def blur_bg_route(payload: BlurBGRequest):
    try:
        result = bria_edit("blur_bg", payload.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))