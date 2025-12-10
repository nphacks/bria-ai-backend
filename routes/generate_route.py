from fastapi import APIRouter
from pydantic import BaseModel
from services.bria_service import generate_image_async


router = APIRouter(prefix="/generate", tags=["Bria Image Generation"])


class PromptRequest(BaseModel):
    prompt: str


@router.post("/")
def generate_image(req: PromptRequest):
    image_url = generate_image_async(req.prompt)
    return {"image_url": image_url}
