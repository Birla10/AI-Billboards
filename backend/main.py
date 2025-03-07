import uvicorn
import asyncio
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from services.websocket_service import start_server
from database.fetch_ads import FirebaseVideoFetcher
from services.perform_ad_search import AdSearch
from services.process_new_ads import ProcessNewAds
from exceptions.video_processing_failed_exception import VideoProcessingFailedException

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start WebSocket server when FastAPI starts."""
    loop = asyncio.get_event_loop()
    loop.create_task(start_server())  # Start WebSocket server in background
    yield  # Run FastAPI after WebSocket is started

# Create FastAPI app
app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False}, lifespan=lifespan)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/endpoint")
async def read_endpoint():
    adSearch = AdSearch()
    try:
        embeds = adSearch.getAccurateAd()
        return JSONResponse(embeds, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ad fetching failed: {str(e)}")

@app.post("/video/")
async def upload_video(file: UploadFile = File(...), keywords: list[str] = Form(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = ProcessNewAds()
    try:
        add_ads.process_ad(file, keywords)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except VideoProcessingFailedException as e:
        raise HTTPException(status_code=500, detail=f"Video upload failed: {str(e)}")

# Run FastAPI using Uvicorn (without asyncio.run)
if __name__ == "__main__":
    uvicorn.run(app)
