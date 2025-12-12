import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BRIA_API_TOKEN = os.getenv("BRIA_API_TOKEN")

EDIT_ENDPOINTS = {
    "erase": "https://engine.prod.bria-api.com/v2/image/edit/erase",
    "gen_fill": "https://engine.prod.bria-api.com/v2/image/edit/gen_fill",
    "remove_bg": "https://engine.prod.bria-api.com/v2/image/edit/remove_background",
    "replace_background": "https://engine.prod.bria-api.com/v2/image/edit/replace_background",
    "blur_bg": "https://engine.prod.bria-api.com/v2/image/edit/blur_background",
    "erase_fg": "https://engine.prod.bria-api.com/v2/image/edit/erase_foreground",
    "expand": "https://engine.prod.bria-api.com/v2/image/edit/expand",
    "enhance": "",
    "upscale": "",
    "crop_fg": "",
}

def bria_edit(operation: str, payload: dict):
    url = EDIT_ENDPOINTS.get(operation)
    if not url:
        raise ValueError(f"Endpoint URL for {operation} not defined.")

    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    resp = requests.post(url, json=payload, headers=headers)
    data = resp.json()
    print("RAW RESPONSE:", resp.text)

    # Async flow
    status_url = data.get("status_url")
    print("Async flow - Status URL:", status_url)
    if status_url:
        return poll_edit_status(status_url)

    # Sync flow
    result = data.get("result", {})
    print("Sync flow - Edit result:", result)
    return {
        "image_url": result.get("image_url"),
        "seed": result.get("seed"),
        "structured_prompt": result.get("structured_prompt")
    }

def poll_edit_status(status_url: str):
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    while True:
        status_data = requests.get(status_url, headers=headers).json()
        status = status_data.get("status")

        if status == "COMPLETED":
            result = status_data.get("result", {})
            print("Edit completed with result:", result)
            return {
                "image_url": result.get("image_url"),
                "seed": result.get("seed"),
                "structured_prompt": result.get("structured_prompt")
            }

        if status == "ERROR":
            return {"error": status_data}

        time.sleep(1)
