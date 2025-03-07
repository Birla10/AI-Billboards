import uvicorn
import asyncio
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from services.websocket_service import start_server
from database.fetch_ads import FirebaseVideoFetcher
from services.perform_ad_search import AdSearch
from services.process_new_ads import ProcessNewAds
from exceptions.video_processing_failed_exception import VideoProcessingFailedException

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

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
        video_fetcher = FirebaseVideoFetcher()
        urls = video_fetcher.fetch_videos()
        embeds = adSearch.getAccurateAd()
        return JSONResponse(urls, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ad fetching failed: {str(e)}")

@app.post("/video/")
async def upload_video(file: UploadFile = File(...), keywords : list[str] = Form(...)):
    """
    Endpoint to upload a video file.
    """
    add_ads = ProcessNewAds()
    try:
        add_ads.process_ad(file, keywords)
        return JSONResponse(content={"message": "Video uploaded successfully!"})
    except VideoProcessingFailedException as e:
        raise HTTPException(status_code=500, detail=f"Video upload failed: {str(e)}")

async def main():
    """
    Run FastAPI and WebSocket server concurrently in the same event loop.
    """
    loop = asyncio.get_event_loop()
    
    # Start the WebSocket server as a background task
    loop.create_task(start_server())

    # Run FastAPI (Uvicorn)
    config = uvicorn.Config(app)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main()) 