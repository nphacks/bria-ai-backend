from fastapi import APIRouter
from pydantic import BaseModel
from services.bria_service import submit_async_request, poll_status


router = APIRouter(prefix="/generate/prompt", tags=["Text Generation"])


class PromptRequest(BaseModel):
    prompt: str


@router.post("/")
def generate_image(req: PromptRequest):
    print("Received prompt for image with prompt:", req.prompt)
    payload = {
        "prompt": req.prompt,
        "sync": False
    }

    data = submit_async_request(payload)
    return poll_status(data["status_url"])
