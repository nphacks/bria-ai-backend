import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env variables

BRIA_API_TOKEN = os.getenv("BRIA_API_TOKEN")
GENERATE_URL = "https://engine.prod.bria-api.com/v2/image/generate"


def generate_image_async(prompt: str):
    if not BRIA_API_TOKEN:
        raise ValueError("BRIA_API_TOKEN is missing. Add it to your .env file.")

    headers = {
        "Content-Type": "application/json",
        "api_token": BRIA_API_TOKEN
    }

    payload = {
        "prompt": prompt,
        "sync": False
    }

    # Step 1: Submit async request
    resp = requests.post(GENERATE_URL, headers=headers, json=payload)
    data = resp.json()

    status_url = data["status_url"]
    request_id = data["request_id"]

    # Step 2: Poll for status
    while True:
        status_resp = requests.get(status_url, headers=headers)
        status_data = status_resp.json()
        status = status_data.get("status")

        if status == "COMPLETED":
            return status_data["result"]["image_url"]

        elif status == "ERROR":
            raise Exception(status_data.get("error"))

        elif status == "UNKNOWN":
            raise Exception("UNKNOWN error. Request ID: " + request_id)

        time.sleep(1)
