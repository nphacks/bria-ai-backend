# routes/edit/structured_description_route.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Union
import requests
import os

router = APIRouter(prefix="/edit/generate_full_descriptions", tags=["Structured output descriptions"])
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class StructuredRequest(BaseModel):
    structured_prompt: Dict[str, Any]


def llm_describe_dict(data: dict) -> str:
    """Call OpenRouter to describe any dict as a paragraph."""
    flattened = "\n".join(f"{k}: {v}" for k, v in data.items() if v is not None)
    prompt = f"Write a single, well-written descriptive paragraph based on the following information:\n{flattened}"

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                # "model": "google/gemma-3n-e2b-it:free",
                "model": "google/gemma-3-4b-it",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        response.raise_for_status()
        output = response.json()
        return output["choices"][0]["message"]["content"].strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenRouter error: {e}")


def process_structured(obj: Any) -> Union[str, list, dict]:
    """
    Recursively process structured prompt:
    - If dict is 'objects': convert each item to LLM description string
    - If dict is other nested object (like aesthetics, lighting, photographic_characteristics): 
      convert to single descriptive string
    - Lists are recursively processed
    - Primitives stay as string
    """
    if isinstance(obj, list):
        return [process_structured(i) for i in obj]

    if isinstance(obj, dict):
        # If this dict is an 'objects' list, handle separately
        if 'objects' in obj:
            result = {}
            for k, v in obj.items():
                if k == "objects" and isinstance(v, list):
                    result[k] = [
                        llm_describe_dict(o) if isinstance(o, dict) else str(o)
                        for o in v
                    ]
                else:
                    # Flatten other dicts like aesthetics, lighting, etc.
                    if isinstance(v, dict):
                        result[k] = llm_describe_dict(v)
                    else:
                        result[k] = str(v)
            return result
        else:
            # Flatten any dicts that are not 'objects'
            result = {}
            for k, v in obj.items():
                if isinstance(v, dict):
                    result[k] = llm_describe_dict(v)
                elif isinstance(v, list):
                    result[k] = [process_structured(i) for i in v]
                else:
                    result[k] = str(v)
            return result

    # Primitive value
    return str(obj)




@router.post("/")
def generate_full_descriptions_route(request: StructuredRequest):
    structured = request.structured_prompt
    return process_structured(structured)
