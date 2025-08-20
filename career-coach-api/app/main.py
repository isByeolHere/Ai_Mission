from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import coach

app = FastAPI(
    title="Career Coach API",
    description="An API that provides personalized career coaching using a generative AI model.",
    version="1.0.0"
)

# Include the v1 router
app.include_router(coach.router, prefix="/api/v1/coach", tags=["Career Coaching"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", tags=["Root"])
async def read_root():
    return FileResponse("static/index.html")

@app.get("/docs", tags=["Documentation"])
async def get_docs():
    return FileResponse("static/index.html")
