from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, model_validator
from typing import List, Optional
from services.bria_edit_service import bria_edit  

router = APIRouter(prefix="/edit/replace_bg", tags=["Replace Background"])

class ReplaceBGRequest(BaseModel):
    image: str
    mode: Optional[str] = "high_control"
    prompt: Optional[str] = None
    ref_images: Optional[List[str]] = None
    enhance_ref_images: Optional[bool] = False
    refine_prompt: Optional[bool] = True
    sync: Optional[bool] = True
    visual_output_content_moderation: Optional[bool] = False
    seed: Optional[int] = None

    @model_validator(mode="before")
    def check_prompt_or_ref_images(cls, values):
        prompt = values.get("prompt")
        ref_images = values.get("ref_images")
        if (not prompt and not ref_images) or (prompt and ref_images):
            raise ValueError("You must provide either prompt or ref_images, but not both.")
        return values


@router.post("/")
def replace_bg_route(payload: ReplaceBGRequest):
    if not payload.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    try:
        payload_dict = {k: v for k, v in payload.dict().items() if v is not None}
        result = bria_edit("replace_background", payload_dict)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

