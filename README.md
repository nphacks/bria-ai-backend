# PlotFrame Backend (FastAPI)

Backend service for PlotFrame, handling image generation/editing via Bria AI and structured-prompt processing via OpenRouter (Gemma).

Setup
1. Install dependencies
```pip install -r requirements.txt```

2. Create .env file

Add the following variables:

`BRIA_API_TOKEN=your_bria_api_token
OPENROUTER_API_KEY=your_openrouter_api_key`

3. Run the server
```uvicorn main:app --reload```


Server runs at:
```http://localhost:8000```

What this backend does

* Proxies Bria AI for image generation & editing
* Uses Gemma (OpenRouter) to process structured image metadata
* Provides endpoints for:
  * Creating characters & shots
  * Editing images (erase, inpaint, remix, etc.)
  * Advanced Remix with structured JSON transformation
