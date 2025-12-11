from fastapi import APIRouter
from pydantic import BaseModel
from services.bria_service import submit_async_request, poll_status


router = APIRouter(prefix="/generate/unified", tags=["Unified Generation"])


class UnifiedRequest(BaseModel):
    prompt: str | None = None
    images: list[str] | None = None
    seeds: list[int] | None = None
    structured_prompts: list[dict] | None = None


@router.post("/")
def unified_generate(req: UnifiedRequest):
    print("Received prompt for image with prompt and images:", req.prompt)
    payload = {
        "prompt": req.prompt,
        "images": req.images,
        "sync": False
    }

    if req.seeds:
        payload["seeds"] = req.seeds

    if req.structured_prompts:
        payload["structured_prompts"] = req.structured_prompts

    data = submit_async_request(payload)
    return poll_status(data["status_url"])
