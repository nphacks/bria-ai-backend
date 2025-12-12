from fastapi import APIRouter
from pydantic import BaseModel
from services.bria_edit_service import bria_edit

router = APIRouter(prefix="/edit/erase", tags=["Image Editing"])

class EraseRequest(BaseModel):
    image: str
    mask: str
    mask_type: str | None = "manual"  # manual or automatic
    preserve_alpha: bool | None = False
    sync: bool | None = False
    visual_input_content_moderation: bool | None = False
    visual_output_content_moderation: bool | None = False

@router.post("/")
def erase(req: EraseRequest):
    payload = req.model_dump()
    return bria_edit("erase", payload)
