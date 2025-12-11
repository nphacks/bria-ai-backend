import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

BRIA_API_TOKEN = os.getenv("BRIA_API_TOKEN")
GENERATE_URL = "https://engine.prod.bria-api.com/v2/image/generate"


def submit_async_request(payload: dict):
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    resp = requests.post(GENERATE_URL, headers=headers, json=payload)
    return resp.json()


def poll_status(status_url: str):
    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    while True:
        status_data = requests.get(status_url, headers=headers).json()
        status = status_data.get("status")

        if status == "COMPLETED":
            return {
                "image_url": status_data["result"]["image_url"],
                "seed": status_data["result"].get("seed"),
                "structured_prompt": status_data["result"].get("structured_prompt")
            }

        if status == "ERROR":
            return {"error": status_data}

        time.sleep(1)
