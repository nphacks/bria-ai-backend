from fastapi import FastAPI
from routes.generate_route import router as generate_router

app = FastAPI()

# Register routes
app.include_router(generate_router)

@app.get("/")
def root():
    return {"message": "Bria FastAPI Server is running"}
