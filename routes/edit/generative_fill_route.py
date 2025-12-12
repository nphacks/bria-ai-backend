from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/gen_fill", tags=["Generative Fill Editing"])

class GenFillRequest(BaseModel):
    image: str
    mask: str
    prompt: str
    version: int | None = 2
    refine_prompt: bool | None = True
    negative_prompt: str | None = None
    seed: int | None = None
    preserve_alpha: bool | None = False
    sync: bool | None = True
    prompt_content_moderation: bool | None = True
    visual_input_content_moderation: bool | None = False
    visual_output_content_moderation: bool | None = False
    tailored_model_id: str | None = None
    mask_type: str | None = "manual"

@router.post("/")
def gen_fill_route(payload: GenFillRequest):
    try:
        result = bria_edit("gen_fill", payload.dict(exclude_none=True))
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
