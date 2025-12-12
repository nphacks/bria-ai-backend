from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.generate_text_route import router as prompt_router
from routes.generate_unified_route import router as unified_router

# editing routes
from routes.edit.erase_route import router as erase_router
from routes.edit.generative_fill_route import router as genfill_router
from routes.edit.remove_bg_route import router as remove_bg_router
from routes.edit.replace_bg_route import router as replace_bg_router
from routes.edit.blur_bg_route import router as blur_bg_router
from routes.edit.erase_fg_route import router as erase_fg_router
from routes.edit.expand_route import router as expand_router
# from routes.edit.enhance_route import router as enhance_router
# from routes.edit.upscale_route import router as upscale_router
# from routes.edit.crop_fg_route import router as crop_fg_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# generation
app.include_router(prompt_router)
app.include_router(unified_router)

# editing
app.include_router(erase_router)
app.include_router(genfill_router)
app.include_router(remove_bg_router)
app.include_router(replace_bg_router)
app.include_router(blur_bg_router)
app.include_router(erase_fg_router)
app.include_router(expand_router)
# app.include_router(enhance_router)
# app.include_router(upscale_router)
# app.include_router(crop_fg_router)