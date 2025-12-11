from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.generate_text_route import router as text_router
from routes.generate_unified_route import router as unified_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(text_router)
app.include_router(unified_router)
